from .base_settings import *

DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
    
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
]
