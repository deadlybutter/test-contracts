# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template
from test_contracts.public.forms import LoginForm
from test_contracts.settings import ProdConfig
from test_contracts.assets import assets
from test_contracts.extensions import (
    cache,
    db,
    migrate,
    debug_toolbar,
    security,
    moment,
    user_datastore,
    admin
)
from test_contracts import public, manage, help, chat, contract, message


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    security.init_app(app, user_datastore, login_form=LoginForm)
    admin.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(manage.views.blueprint)
    app.register_blueprint(help.views.blueprint)
    app.register_blueprint(chat.views.blueprint)
    app.register_blueprint(contract.views.blueprint)
    app.register_blueprint(message.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None