#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask_script import Manager, Shell, Server, Command, Option
from flask_migrate import MigrateCommand
from test_contracts.app import create_app
from test_contracts.models import User
from test_contracts.settings import DevConfig, ProdConfig
from test_contracts.database import db


if os.environ.get("TESTIE_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test():
    """Run the tests."""
    import pytest

    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


@manager.command
def data(test=False, prod=False):
    """Add production data or test filler data."""
    if test:
        import data.test.careers
        import data.test.users
        import data.test.contracts
        import data.test.faq
        import data.test.static
    if prod:
        import data.prod.interests
        import data.prod.crewroles
        import data.prod.servicecategory
        import data.prod.services
        import data.prod.manufacturer
        import data.prod.roles
        import data.prod.ships


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
