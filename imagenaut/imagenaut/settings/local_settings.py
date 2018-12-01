from .base_settings import *

DEBUG = True
THUMBNAIL_DEBUG = True
REST_VALIDATOR_SINGLE_USE = False

INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar',]
    
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
]

CAPTCHA_TEST_MODE = True
