# -*- coding: utf-8 -*-
__author__ = ''

from aap_whatsapp.model.message import Message, User,MessageReceived
from aap_whatsapp import ma
from aap_whatsapp.schemas import safe_execute


class MessageReceivedSchema(ma.ModelSchema):
    user = ma.Nested('UserSchema', exclude=('messages_received',))
    message = ma.Nested('MessageSchema', exclude=('received_from_users',))

    class Meta:
        model = MessageReceived
        exclude = ('created_at', 'updated_at')


class MessageSchema(ma.ModelSchema):
    received_from_users = ma.Nested('MessageReceivedSchema', many=True, exclude=('messages_received','message'))

    class Meta:
        model = Message
        exclude = ('created_at', 'updated_at')


class UserSchema(ma.ModelSchema):
    messages_received = ma.Nested('MessageReceivedSchema', many=True, exclude=('received_from_users', 'user'))

    class Meta:
        model = User
        exclude = ('created_at', 'updated_at', 'received_messages')
