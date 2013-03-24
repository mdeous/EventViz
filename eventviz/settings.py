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

# EventViz settings
JS_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S'
DEBUG_PARSERS = False

try:
    from prod_settings import *
except ImportError:
    pass
