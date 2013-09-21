from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('vivyly', 'vivyly9@gmail.com'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'parcellate',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}