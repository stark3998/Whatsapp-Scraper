# -*- coding: utf-8 -*-

CLASSES = {
    'chat_contact': '_25Ooe',                                        # contacts in contact list (left side)(inner-elem)
    'is_chat': 'RLfQR',                                              # chat or contact presence in the chat-list
    'chat_body': '_1_keJ',                                           # chat body of contact
    'html_attribute': {'ml': 'innerHTML',                            # soup html attribute
                       'ml_type': 'html.parser'},
}
IDS = {
    'chat_panel': 'pane-side',                                       # contacts in contact list (left side)
    'chatlist_search': 'input-chatlist-search'                       # contact list (left panel)
}
CSS = {
    'chatlist_search': '_2zCfw.copyable-text.selectable-text',             # contact list (left panel)
    'msg_box': '._2S1VP.copyable-text.selectable-text',                    # message box in whatsapp
    'header_click': '._1WBXd',                                             # header class from channel information
    'contact_info': '._2fq0t.copyable-area',                               # group or contact information page
    'delete_chat': '._10anr.vidHz._28zBA',                                 # delete chat button from menu option
    'ok_delete': '._1WZqU.PNlAR',                                          # confirm delete after delete chat button
    'gallery': '._10anr.vidHz._3asN5',                                     # gallery button
    'caption': '._2S1VP.copyable-text.selectable-text'
}


ELS = {
    'chat_contact': {"el": "div",                                         # title of contact in contact list (left side)
                     "el_class": {"class": "_25Ooe"}},
    'contacts_class': {"el": "div",                                       # contact class in contact list (left side)
                       "el_class": {"class": "_2WP9Q"}},
    'contact_list': {"el": "div",                                         # group participants name list
                     "el_class": {"class": "_2wP_Y"}},
    'participants': {"el": "div",                                         # total length of participants in group
                     "el_class": {"class": "_1CRb5 _34vig",
                                  'data-list-scroll-offset': 'true'}},
    'contact_len': {"el": "span",                                         # number of participants (only numbers)
                    "el_class": {"class": "_1sYdX"}},
    'sender_obj': {"el": "span",                                          # sender obj in the group contact lists
                   "el_class": {"class": "ellipsify screen-name"}},
    'number_obj': {"el": "span",                                          # number obj in the group contact lists
                   "el_class": {"class": "_1wjpf"}},
    'msg': {"el": "div",                                                  # messages in chat body
            "el_class": {"class": "FTBzM"}},
    'number_obj_user': {"el": 'span',                                     # number obj of user from contact info page
                        "el_class": {'class': 'selectable-text invisible-space copyable-text'}},
    'msg_content': {"el": "span",                                         # for all message data in chat
                    "el_class": {"class": "selectable-text invisible-space copyable-text"}},
    'number_obj_msg': {"el": "span",                                      # number obj in message in group chat
                       "el_class": {'class': 'RZ7GO'}},
    'sender_obj_msg': {"el": "span",                                      # sender obj in message in group chat
                       "el_class": {'class': '_3Ye_R _1wjpf _1OmDL'}},
    'send_date_user': {"el": 'div',                                       # send date from message in users chat
                       "el_class": {'class': 'copyable-text'}},
    'send_date_group': {"el": 'div',                                      # send date from message in group chat
                        "el_class": {'class': '_3Usvm copyable-text'}},
    'default_user': {"el": "span",                                        # select only user channels from chat list
                     "el_class": {"data-icon": "default-user"}},
    'default_group': {"el": "span",                                       # select only group channels from chat list
                      "el_class": {"data-icon": "default-group"}},
}

SCROLL = {
    'to_top': "document.getElementById('pane-side').scrollBy(0,-1000000)",
    'left_panel': "document.getElementById('pane-side').scrollBy(0,720)",          # scroll contact-list (left side)
    'chat_page': "document.getElementsByClassName('_1_keJ').scrollBy(0,-10000);",  # scroll chat page of contact
    'info_page': "document.getElementsByClassName('_2sNbV')[0].scrollBy(0,500);"   # scroll group or contact info page
}

