# -*- coding: utf-8 -*-
"""The manage module, including staff management stuff and admin."""
from flask import (url_for, flash, redirect)
from ..extensions import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from test_contracts.models import User, Role, Services, Divisions, Interests, \
    ServiceCategory, Contract, StaticPage, Ships, Manufacturer, Note, Event
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask.ext.admin import base
from . import views


# TODO: Models have changed, go over this when its running to confirm fields.
class AccessView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated(): return False
        return current_user.has_role('Admin')

    def inaccessible_callback(self, name, **kwargs):
        flash('You are not authorized to access this.', 'danger')
        return redirect(url_for('public.home'))


class UserView(AccessView, ModelView):
    column_exclude_list = (
        'reset_password_token', 'confirmed_at', 'avatar_hash', 'password', 'created_at', 'last_login_at',
        'current_login_at', 'last_login_ip', 'current_login_ip', 'login_count', 'first_name', 'last_name', 'website',
        'organization')
    form_excluded_columns = ('password', 'reset_password_token', 'avatar_hash')
    column_searchable_list = (User.username, User.email, User.spectrum, User.handle, User.spectrum)


class RoleView(AccessView, ModelView):
    form_excluded_columns = 'users'


class ServiceView(AccessView, ModelView):
    column_labels = dict(servicecategory="Category")
    column_exclude_list = 'job'
    form_excluded_columns = 'job'


class ContractView(AccessView, ModelView):
    column_searchable_list = (User.username, User.handle, Services.name, Contract.invoice, Contract.code)
    column_labels = dict(code="Code Word", time="Estimated Time", scu="Standard Cargo Units", fuel="Fuel Cargo Units")
    column_exclude_list = ('location', 'description', 'warzone', 'scu', 'Ships',
                           'fuel', 'passengers', 'pilot', 'radar', 'weapons', 'gunner', 'engineer',
                           'navigation', 'communications', 'security', 'science', 'medical')


class ShipsView(AccessView, ModelView):
    column_labels = dict(maxcrew="Maximum Crew Size",
                         scu="Standard Cargo Units",
                         lifesupport="Maximum Crew Life Support Capacity",
                         gunners="Maximum Gunner Positions")
    column_exclude_list = 'contract'
    form_excluded_columns = 'contract'


class ManuView(AccessView, ModelView):
    column_exclude_list = 'ships'
    form_excluded_columns = 'ships'
    column_labels = dict(abbr="Abbreviation")


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class PolicyView(AccessView, ModelView):
    form_overrides = {
        'content': CKTextAreaField
    }

    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    column_labels = dict(name="Page Name")


admin.add_link(base.MenuLink('Back', endpoint='public.home'))
admin.add_view(UserView(User, db.session, category='Users', endpoint='users'))
admin.add_view(RoleView(Role, db.session, category='Users', endpoint='roles'))
admin.add_view(AccessView(Interests, db.session, category='Users', endpoint='interests'))
admin.add_view(ServiceView(Services, db.session, category='Services', endpoint='services'))
admin.add_view(AccessView(ServiceCategory, db.session, category='Services', endpoint='service-category'))
admin.add_view(AccessView(Divisions, db.session, endpoint='divisons'))
admin.add_view(ShipsView(Ships, db.session, category='Ships', endpoint='ships'))
admin.add_view(ManuView(Manufacturer, db.session, category='Ships', endpoint='manufacturer'))
admin.add_view(ContractView(Contract, db.session, name='Contracts', category='Contracts', endpoint='contracts'))
admin.add_view(AccessView(Note, db.session, name='Notes', category='Contracts', endpoint='notes'))
admin.add_view(AccessView(Event, db.session, name='Events', category='Contracts', endpoint='events'))
admin.add_view(PolicyView(StaticPage, db.session, name='Static Pages', category='Settings', endpoint='static'))
