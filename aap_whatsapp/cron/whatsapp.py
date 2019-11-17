# -*- coding: utf-8 -*-
import time
import json
from datetime import datetime, timezone
from aap_whatsapp import db
from flask_script import Command
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from aap_whatsapp.constants.crawl_elem import CLASSES, CSS, SCROLL, ELS
from aap_whatsapp.model.message import Message, User, MessageReceived
from aap_whatsapp.api.user import create_user
from aap_whatsapp import logging
from bs4 import BeautifulSoup
import re
import os

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

cwd = os.getcwd()


class Whatsapp(Command):

    def run(self):
        logging.info("Script Started")
        _chrome_options = webdriver.ChromeOptions()
        _chrome_options.add_argument("--disable-infobars")
        _chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(cwd + '/aap_whatsapp/driver/chromedriver', chrome_options=_chrome_options)
        driver.get("https://web.whatsapp.com")
        # self.set_storage(driver)
        WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.XPATH,"//*[@id=\"side\"]/div[1]/div/label/input")))
        logging.info("LoggedIn to WhatsApp")
        # ls = driver.execute_script("return {...window.localStorage}")
        # with open('creds.json', 'w') as outfile:
        #     json.dump(dict(ls), outfile, indent=4)
        while True:
            messages = Message.query.filter_by(is_active=True).all()
            logging.info("Total Active Messages found {0}".format(len(messages)))
            driver.execute_script(SCROLL['to_top'])
            try:
                search_bar=driver.find_element_by_xpath("//*[@id=\"side\"]/div[1]/div/label/input")
            except Exception as error:
                print(error)
            unread = []
            logging.info("Extracting unread chats")


            for i in range(100):
                chat_list = driver.find_element_by_id('pane-side')
                soup = BeautifulSoup(chat_list.get_attribute(CLASSES['html_attribute']['ml']),
                                     CLASSES['html_attribute']['ml_type'])
                chats = soup.find_all(ELS['contacts_class']['el'], ELS['contacts_class']['el_class'])
                
                for c in chats:
                    if c.find("span", "P6z4j"):
                        try:
                            count = str(c.find('span', "P6z4j")).split(">")[1].split("<")[0]
                            print("Count",count)
                        except:
                            print("Count Error")

                        if count:
                            count = int(count)
                        else:
                            count = 1
                        person = c.find("span", "_19RFN")
                        print("Person",person)
                        unread.append((person['title'], int(str(count))))
                driver.execute_script(SCROLL['left_panel'])
            print(unread)


            unread = set(unread)
            logging.info("unread chats ({0}) in format (person,unread_count) -> {1}".format(len(unread), unread))
            for person in unread:
                try:
                    logging.info("extracting chat for person {0}".format(person))
                    search_bar.clear()
                    search_bar.send_keys(person[0])
                    search_bar.send_keys(Keys.ENTER)
                    chat_body = driver.find_element_by_class_name(CLASSES['chat_body'])
                    chat_soup = BeautifulSoup(chat_body.get_attribute(CLASSES['html_attribute']['ml']),
                                              CLASSES['html_attribute']['ml_type'])
                    msgs = chat_soup.find_all(ELS['msg']['el'], ELS['msg']['el_class'])
                    # if len(msgs) < int(person[1]):
                    #     print("scroll")
                    logging.info("Unread Messages are:")
                    for m in msgs[-int(person[1]):]:
                        msg_text = m.find("span", "selectable-text invisible-space copyable-text").text
                        logging.info(msg_text)
                        for db_msg in messages:
                            diff = int((datetime.now(timezone.utc) - db_msg.created_at).days)
                            print("Difference between Days : ", diff)
                            if (diff >= 3):
                                print("Setting Message as Inactive")
                                db_msg.is_active = False
                                db_msg.update()
                                continue
                            logging.info("matching with {0} from DB".format(db_msg))
                            line_count = 0
                            match_count = 0
                            b = emoji_pattern.sub(r'', msg_text).replace("\n", " ").split(" ")
                            a = emoji_pattern.sub(r'', db_msg.text).replace("\n", " ").split(" ")
                            count = 0
                            for x in a:
                                if x in b:
                                    count += 1
                            print(" Match Count : ", count)
                            print(" Match accuracy : ", (count / len(a)) * 100)
                            if (count / len(a)) * 100 >= 80:
                                match_count = 1

                            if match_count:
                                logging.info("[MATCHED] in {0}".format(person[0]))
                                if person[0][0] != "+":
                                    u = User.query.filter_by(name=person[0]).first()
                                    if not u:
                                        logging.info("Creating Entry in DB for user {0}", person[0])
                                        u = create_user(name=person[0])
                                else:
                                    u = User.query.filter_by(number=person[0][3:].replace(" ", "")).first()
                                    if not u:
                                        logging.info("Creating Entry in DB for user with number {0}",
                                                     int(person[0][3:].replace(" ", "")))
                                        u = create_user(name="", number=int(person[0][3:].replace(" ", "")))
                                if u:
                                    ob = None
                                    logging.info("Updating Receive Info")
                                    if db_msg.received_from_users:
                                        for usr in db_msg.received_from_users:
                                            if u.id == usr.user.id:
                                                ob = MessageReceived.query.filter_by(user_id=u.id,
                                                                                     message_id=db_msg.id).first()
                                                ob.receive_count += 1
                                                ob.save()
                                                logging.info(
                                                    "Increased receive count for {0}. New RecieveCount={1}".format(
                                                        u.name, ob.receive_count))
                                                break
                                    if not ob:
                                        logging.info("Creating Entry in received for user {0}".format(u.name))
                                        ob = MessageReceived(user_id=u.id, message_id=db_msg.id)
                                        db_msg.received_from_users.append(ob)
                                        db_msg.save()
                except Exception as e:
                    logging.exception(e)
            driver.execute_script(SCROLL['to_top'])
            logging.info("Sleep for 1 Min")
            time.sleep(60)

    @staticmethod
    def set_storage(driver):
        if os.path.exists(cwd + '/creds.json'):
            with open('creds.json', 'r') as creds:
                d = json.load(creds)
                for key in d:
                    if key == "storage_test":
                        continue
                    try:
                        script = "window.localStorage.setItem('{0}',JSON.stringify({1}));".format(key, d[key])
                        driver.execute_script(script)
                    except Exception as e:
                        logging.exception(e)
            driver.refresh()
