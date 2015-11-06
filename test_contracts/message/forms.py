# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from test_contracts.models import User
from test_contracts.utils import flash_errors


class Message(Form):
    subject = StringField("Subject", [DataRequired("You forgot to include a subject!")])
    body = TextAreaField("Body", [DataRequired("You forgot to include a message!")])
    submit = SubmitField(label='Submit')


class ModalMessage(Message):
    recipient = HiddenField("To", [DataRequired("You forgot to tell us who to send this to!")])

    def validate_recipient(self, field):
        _recipient = User.query.filter(User.username == self.recipient.data).first()
        if _recipient is None:
            raise ValidationError('Invalid Recipient')


class EmbeddedMessage(Message):
    recipient = StringField("To", [DataRequired("You forgot to tell us who to send this to!")])

    def validate_recipient(self, field):
        _recipient = User.query.filter(User.username == self.recipient.data).first()
        if _recipient is None:
            raise ValidationError('Invalid Recipient')