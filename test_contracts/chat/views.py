from datetime import datetime as dt
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_security import login_required, current_user, roles_accepted
from test_contracts.utils import flash_errors, add_event, add_note
from test_contracts.models import Contract, Services, Faq


blueprint = Blueprint("chat", __name__, url_prefix='/chat',
                      static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def chat():
    return render_template('chat/chat.html')