# -*- coding: utf-8 -*-
"""Manage section"""
from flask import (Blueprint, request, render_template, flash, url_for, redirect, g)
from flask_security import current_user, login_required, roles_accepted
from test_contracts.extensions import db, user_datastore
from test_contracts.message.forms import ModalMessage, EmbeddedMessage
from test_contracts.models import Messages
from test_contracts.utils import flash_errors, send_message
from sqlalchemy import or_
from datetime import datetime as dt


blueprint = Blueprint("message", __name__, url_prefix='/message',
                      static_folder="../static")


@blueprint.before_request
def before_request():
    if current_user.is_authenticated():
        g.new = Messages.query.filter(Messages.recipient_id == current_user.id,
                                      Messages.user_for_id == current_user.id,
                                      Messages.unread == True).count()
    else:
        g.new = None


@blueprint.route("/_send_message/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def _send_message():
    _message = ModalMessage()
    if request.method == 'POST':
        if _message.validate_on_submit():
            send_message(sender=current_user.id, recipient=_message.recipient.data, subject=_message.subject.data,
                         body=_message.body.data)
        else:
            flash_errors(_message)
    return redirect(url_for('message.new'))


# Send Message
@blueprint.route("/new/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def new():
    _embedded = EmbeddedMessage()
    if request.method == 'POST':
        if _embedded.validate_on_submit():
            send_message(sender=current_user.id, recipient=_embedded.recipient.data,
                         subject=_embedded.subject.data,
                         body=_embedded.body.data)
            return redirect(url_for('message.sent'))
        else:
            flash_errors(_embedded)
    return render_template("message/new.html", _embedded=_embedded)


# Inbox
@blueprint.route("/", defaults={'page': 1}, methods=["GET"])
@blueprint.route("/inbox/", defaults={'page': 1}, methods=["GET"])
@blueprint.route("/inbox/<int:page>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def inbox(page):
    _message = ModalMessage()
    inbox_messages = Messages.query.filter(Messages.recipient_id == current_user.id,
                                           Messages.user_for_id == current_user.id,
                                           Messages.draft != 1,
                                           Messages.trash != 1).paginate(
        page, 10, True)
    time = dt.utcnow()
    return render_template("message/inbox.html", inbox_messages=inbox_messages, time=time, _message=_message)


# Sent
@blueprint.route("/sent/", defaults={'page': 1}, methods=["GET"])
@blueprint.route("/sent/<int:page>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def sent(page):
    _message = ModalMessage()
    sent_messages = Messages.query.filter(Messages.sender_id == current_user.id,
                                          Messages.user_for_id == current_user.id,
                                          Messages.draft != 1,
                                          Messages.trash != 1).paginate(
        page, 10, True)
    time = dt.utcnow()
    return render_template("message/sent.html", sent_messages=sent_messages, time=time, _message=_message)


# Draft
@blueprint.route("/draft/", defaults={'page': 1}, methods=["GET"])
@blueprint.route("/draft/<int:page>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def draft(page):
    draft_messages = Messages.query.filter(Messages.sender_id == current_user.id,
                                           Messages.user_for_id == current_user.id,
                                           Messages.draft == 1).paginate(
        page, 10, True)
    time = dt.utcnow()
    return render_template("message/draft.html", draft_messages=draft_messages, time=time)


# trash
@blueprint.route("/trash/", defaults={'page': 1}, methods=["GET"])
@blueprint.route("/trash/<int:page>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def trash(page):
    _message = ModalMessage()
    time = dt.utcnow()
    trash_messages = Messages.query.filter(or_(Messages.sender_id == current_user.id,
                                               Messages.recipient_id == current_user.id),
                                           Messages.trash == 1).paginate(
        page, 10, True)
    return render_template("message/trash.html", time=time, trash_messages=trash_messages, _message=_message)


# view message
@blueprint.route("/view/<msg_id>/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def view(msg_id):
    _message = Messages.query.filter(or_(Messages.recipient_id == current_user.id,
                                         Messages.sender_id == current_user.id),
                                     Messages.user_for_id == current_user.id,
                                     Messages.id == msg_id).first()
    time = dt.utcnow()
    if _message is None:
        return redirect(url_for('message.inbox'))
    if _message.recipient == current_user.id:
        _message.update(unread=False, read_at=dt.utcnow())
    else:
        _message.update(unread=False)
    return render_template("message/view.html", message=_message, time=time)


@blueprint.route("/_trash/", defaults={'msg': 0}, methods=["GET"])
@blueprint.route("/_trash/<int:msg>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def _trash(msg):
    if request.method == 'GET':
        _message = Messages.query.filter(Messages.id == msg,
                                         Messages.user_for_id == current_user.id).first_or_404()
        if _message is None:
            return redirect(url_for('message.trash'))
        else:
            _message.update(trash=1)
            flash('Message moved to trash.', 'info')
            return redirect(url_for('message.trash'))
    else:
        return redirect(url_for('message.trash'))


@blueprint.route("/_delete/", defaults={'msg': 0}, methods=["GET"])
@blueprint.route("/_delete/<int:msg>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def _delete(msg):
    if request.method == 'GET':
        _message = Messages.query.filter(Messages.id == msg,
                                         Messages.user_for_id == current_user.id).first_or_404()
        if _message is None:
            return redirect(url_for('message.trash'))
        else:
            _message.delete()
            flash('Message has been permanently deleted.', 'info')
            return redirect(url_for('message.trash'))
    else:
        return redirect(url_for('message.trash'))


@blueprint.route("/_send_draft/", defaults={'msg': 0}, methods=["GET"])
@blueprint.route("/_send_draft/<int:msg>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def _send_draft(msg):
    if request.method == 'GET':
        _message = Messages.query.filter(Messages.id == msg,
                                         Messages.user_for_id == current_user.id,
                                         Messages.draft == 1).first_or_404()
        if _message is None:
            return redirect(url_for('message.draft'))
        else:
            send_message()
            flash('Message has been permanently deleted.', 'info')
            return redirect(url_for('message.draft'))
    else:
        return redirect(url_for('message.draft'))


@blueprint.route("/_return/", defaults={'msg': 0}, methods=["GET"])
@blueprint.route("/_return/<int:msg>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def _return(msg):
    if request.method == 'GET':
        _message = Messages.query.filter(Messages.id == msg,
                                         Messages.trash == 1,
                                         Messages.user_for_id == current_user.id).first_or_404()
        if _message is None:
            return redirect(url_for('message.trash'))
        else:
            _message.update(trash=0)
            flash('Message has been returned.', 'info')
            return redirect(url_for('message.trash'))
    else:
        return redirect(url_for('message.trash'))