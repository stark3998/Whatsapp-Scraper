# -*- coding: utf-8 -*-
from aap_whatsapp import db
from aap_whatsapp.model.base import Base


class MessageReceived(db.Model):
    __tablename__ = 'message_received'
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    receive_count = db.Column(db.Integer, default=1)

    message = db.relationship("Message", backref="received_from_users")
    user = db.relationship("User", backref="messages_received")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class User(Base):
    __tablename__ = 'user'
    name = db.Column(db.String(50))
    number = db.Column(db.BigInteger, unique=True)
    broadcast_count = db.Column(db.Integer)

    received_messages = db.relationship("Message", secondary="message_received")


class Message(Base):
    __tablename__ = 'message'
    text = db.Column(db.Text)
    is_active = db.Column(db.BOOLEAN, default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "<{}>".format(self.text)
