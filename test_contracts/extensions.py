# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()

from flask_cache import Cache
cache = Cache()

from flask_security import SQLAlchemyUserDatastore
from test_contracts.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

from flask_security import Security
security = Security()

from flask.ext.moment import Moment
moment = Moment()

from flask_debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()

from flask_admin import AdminIndexView, expose
from flask_security import current_user
from flask import redirect, url_for, flash


class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    def inaccessible_callback(self, name, **kwargs):
        flash('You are not authorized to access this.', 'danger')
        return redirect(url_for('public.home'))

    def is_accessible(self):
        if not current_user.is_authenticated(): return False
        return current_user.has_role('Admin')


from flask_admin import Admin
admin = Admin(index_view=AdminView(), name="Admin", template_mode='bootstrap3')

