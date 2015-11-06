# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for, redirect, after_this_request, g)
from flask_security import login_user, logout_user, current_user, login_required, roles_accepted
from test_contracts.extensions import db, user_datastore
from test_contracts.models import Services, Divisions, StaticPage, User, Messages
from test_contracts.public.forms import LoginForm, RegisterForm, EditProfile
from test_contracts.utils import flash_errors


blueprint = Blueprint('public', __name__, static_folder="../static")


def _commit(response=None):
    user_datastore.commit()
    return response


@blueprint.before_request
def before_request():
    if current_user.is_authenticated():
        g.new = Messages.query.filter(Messages.recipient_id == current_user.id,
                                      Messages.user_for_id == current_user.id,
                                      Messages.unread == True).count()
    else:
        g.new = None


# Main Page
@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    return render_template("public/home.html", form=form)


# Login
@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            after_this_request(_commit)
            flash("You are now logged in.", 'success')
            if request.args.get("next"):
                return redirect(request.args.get("next"))
            else:
                return redirect(url_for('public.overview'))
        else:
            flash_errors(form)
    return render_template("public/login.html", form=form)


# Logout
@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('public.home'))


# Register
# TODO: Discussion: Registration - Disabled, invite only or default contractor.
# Decide on disabling registration and switching to an invite only system, adding an invite code or
# keeping open registration that defaults as a non-employee contractor.
@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        default_role = user_datastore.find_role('Contractor')
        new_user = user_datastore.create_user(username=form.username.data,
                                              email=form.email.data,
                                              password=form.password.data)
        user_datastore.add_role_to_user(new_user, default_role)
        db.session.commit()
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


# Services
# TODO:  Discussion:  Should this be divided by division?
@blueprint.route("/services/")
def services():
    form = LoginForm(request.form)
    _services = Services.query.all()
    return render_template("public/services.html", form=form, services=_services)


# Careers
# TODO:  Discussion:  Should this be switched to divisions?
@blueprint.route("/divisions/")
def divisions():
    form = LoginForm(request.form)
    _divisions = Divisions.query.all()
    return render_template("public/divisions.html", form=form, divisions=_divisions)


# About
# TODO:  Write something witty.
@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


# TODO:  To be moved to help.
@blueprint.route("/contact/")
def contact():
    form = LoginForm(request.form)
    return render_template("public/contact.html", form=form)


# Terms of Service
@blueprint.route("/tos/")
def tos():
    form = LoginForm(request.form)
    content = StaticPage.query.filter_by(name='tos').first()
    return render_template("public/tos.html", form=form, content=content)


# Insurance policy
@blueprint.route("/insurance/")
def insurance():
    form = LoginForm(request.form)
    content = StaticPage.query.filter_by(name='insurance').first()
    return render_template("public/insurance.html", form=form, content=content)


# Privacy Policy
@blueprint.route("/privacy/")
def privacy():
    form = LoginForm(request.form)
    content = StaticPage.query.filter_by(name='privacy').first()
    return render_template("public/privacy.html", form=form, content=content)


# Settings for all users
@blueprint.route("/settings/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def settings():
    form = EditProfile()
    user = User.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.website = form.website.data
            current_user.organization = form.organization.data
            current_user.spectrum = form.spectrum.data
            current_user.handle = form.handle.data
            current_user.interests = form.interests.data
            db.session.add(user)
            db.session.commit()
            flash('Your settings has been updated.', 'info')
            return redirect(url_for('public.profile'))
        else:
            flash_errors(form)
    form.email.data = current_user.email
    form.website.data = current_user.website
    form.organization.data = current_user.organization
    form.spectrum.data = current_user.spectrum
    form.handle.data = current_user.handle
    form.interests.data = current_user.interests
    return render_template("public/profile.html", form=form)


# Overview page for all users and roles
@blueprint.route("/overview/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def overview():
    return render_template("public/overview.html")