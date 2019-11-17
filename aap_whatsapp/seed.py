# -*- coding: utf-8 -*-
import csv
from flask_script import Command
from aap_whatsapp.model.message import User
from aap_whatsapp import db


class SeedData(Command):
    def run(self):
        with open('users.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                t = row[0], row[1], row[2]
                print(t)
                u = User(name=row[0], number=row[1], broadcast_count=row[2])
                u.save()
