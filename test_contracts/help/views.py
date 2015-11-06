# -*- coding: utf-8 -*-
"""Help section"""
from flask import (Blueprint, request, render_template, flash, url_for, redirect, after_this_request)
from flask_security import current_user, login_required, roles_accepted
from test_contracts.extensions import db, user_datastore
from test_contracts.models import Contract, Faq
from test_contracts.utils import flash_errors


blueprint = Blueprint("help", __name__, url_prefix='/help',
                      static_folder="../static")


# TODO: Manage users for staff
@blueprint.route("/faq/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def faq():
    _faq = Faq.query.filter(Faq.active == 1).all()
    return render_template("help/faq.html", faq=_faq)


# TODO: Arbiter stuff.
@blueprint.route("/arbiter/", methods=["GET"])
@login_required
@roles_accepted('Arbiter', 'Staff', 'Admin')
def arbiter():
    return render_template("help/arbiter.html")