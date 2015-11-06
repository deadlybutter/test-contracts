# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from datetime import datetime as dt
from test_contracts.extensions import db
from test_contracts.models import Note, Contract, Event, Messages, User


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)


def add_note(note, user, invoice, staff=1, contractor=1, client=1):
    j = Contract.query.filter(Contract.invoice == invoice).first()
    n = Note.create(time=dt.utcnow(), note=note, user_id=user, staff_flag=staff, contractor_flag=contractor,
                    client_flag=client)
    j.notes.append(n)
    db.session.commit()


def add_event(event, user, invoice, staff=1, contractor=1, client=1):
    j = Contract.query.filter(Contract.invoice == invoice).first()
    e = Event.create(time=dt.utcnow(), event=event, user_id=user, staff_flag=staff, contractor_flag=contractor,
                     client_flag=client)
    j.events.append(e)
    db.session.commit()


def send_message(sender, recipient, subject, body):
    _sender = User.query.filter_by(id=sender).first()
    _recipient = User.query.filter_by(username=recipient).first()
    _msg_recipient = Messages.create(user_for=_recipient, sender=_sender, recipient=_recipient, subject=subject,
                                     body=body, sent_at=dt.utcnow())
    _msg_sender = Messages.create(user_for=_sender, sender=_sender, recipient=_recipient, subject=subject,
                                  body=body, sent_at=dt.utcnow())
    db.session.commit()
    flash('Message Sent.', 'success')


def save_message(sender, recipient, subject, body):
    _sender = User.query.filter_by(id=sender).first()
    _recipient = User.query.filter_by(username=recipient).first()
    Messages.create(sender=_sender.id, recipient=_recipient.id, subject=subject,
                    body=body, draft=True)
    db.session.commit()
    flash('Message saved.', 'success')