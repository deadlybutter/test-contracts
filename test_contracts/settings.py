# -*- coding: utf-8 -*-
import os

os_env = os.environ


class Config(object):
    SECRET_KEY = os_env.get('TESTIE_SECRET', 'not-so-secret')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'saltytearspowergears'
    SECURITY_LOGIN_SALT = 'yarrrr?'
    SECURITY_UNAUTHORIZED_VIEW = 'public.home'
    SECURITY_REGISTERABLE = 'False'
    SECURITY_TRACKABLE = 'True'
    SECURITY_LOGIN_URL = '/login'
    SECURITY_CHANGE_URL = '/change/'
    SECURITY_CONFIRM_URL = '/confirm/'
    SECURITY_POST_LOGIN_VIEW = 'public.overview'
    SECURITY_POST_LOGOUT_VIEW = 'public.home'
    SECURITY_POST_REGISTER_VIEW = 'public.home'


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    TESTIE_USER = os_env.get('TESTIE_USER')
    TESTIE_PASS = os_env.get('TESTIE_PASS')
    TESTIE_DB = os_env.get('TESTIE_DB')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@localhost/{2}'.format(TESTIE_USER, TESTIE_PASS, TESTIE_DB)
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    SECURITY_CONFIRMABLE = 'False'
    SECURITY_RECOVERABLE = 'True'
    SECURITY_CHANGEABLE = 'False'  # DEMO ONLY CHANGE ME LATER!


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

    def __lt__(self, *args, **kwargs):
        return super().__lt__(*args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        return super().__reduce_ex__(*args, **kwargs)

    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SECURITY_CONFIRMABLE = 'False'
    SECURITY_RECOVERABLE = 'True'
    SECURITY_CHANGEABLE = 'False'


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
