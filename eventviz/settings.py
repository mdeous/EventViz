# -*- coding: utf-8 -*-

# Flask settings
DEBUG = True
SECRET_KEY = 'CHANGEME'
SESSION_COOKIE_NAME = '_session'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

# Database settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'test_project'

try:
    from prod_settings import *
except ImportError:
    pass
