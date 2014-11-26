# Django AWS Elastic Beanstalk Site Specific Project file
# All non site specific settings should go into the settings.py file

# For local dev, use settings_local.py. When doing a deploy to beanstalk, set the DJANGO_SETTINGS_MODULE to this file:  (settings_beanstalk)
# This file relies on your settings as defined in your beanstalk environment properties which are passed into the application as environment variables.
# These can be found under your-environment on the beanstalk -> configuration -> software configuration

import os
from settings import *

SITE_NAME = os.environ['SITE_NAME'] # i.e. staging


PRODUCTION_SITES = ['live', 'staging']

DEBUG = (os.environ.get('DEBUG', False) == 'True')

ALLOWED_HOSTS = [
    '.trapeze.com',
    '.unioncreative.com',
    '.elasticbeanstalk.com',
    '.amazonaws.com',
    '.your-domain.com',
]

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  # should be unique

DEFAULT_FROM_EMAIL = 'noreply@your-domain.com'

# Uncomment on local development if debug is False.
# This will overwrite the common setting that points to the alert mailbox.
#ADMINS = (('Django Alerts', '<email>'))
try:
    CONN_MAX_AGE = int(os.environ.get('CONN_MAX_AGE', 0))
except ValueError:
    CONN_MAX_AGE = 0


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  #.psycopg2
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
        'CONN_MAX_AGE': CONN_MAX_AGE,
        'OPTIONS': {
            'autocommit': True,
        },
    }
}

try:
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', 300))
except ValueError:
    CACHE_TIMEOUT = 300

CACHE_LOCATION = os.environ.get('CACHE_LOCATION')

if CACHE_LOCATION:
    CACHES = {
        'default': {
            'BACKEND': 'calm_cache.backends.CalmCache',
            'LOCATION': 'base',
            'KEY_FUNCTION': 'calm_cache.contrib.sha1_key_func',
            'KEY_PREFIX': '%s:%s' % (SITE_NAME, RELEASE),
            'OPTIONS': {
                'MINT_PERIOD': '10',        # Allow stale results for this many seconds. Default: 0 (Off)
                'GRACE_PERIOD': '120',      # Serve stale value once during this period. Default: 0 (Off)
                'JITTER': '10',             # Upper bound on the random jitter in seconds. Default: 0 (Off)
            },
        },
        'base': {
            'BACKEND': 'django_elasticache.memcached.ElastiCache',
            'LOCATION': CACHE_LOCATION,
        },
    }

else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }

    }

# Django needs to know the version number, otherwise it tries to make an
# initial connection to postgres before running management commands.
POSTGIS_VERSION = (2, 0, 1)

STATIC_URL = os.environ['DJANGO_STATIC_URL']
MEDIA_URL = os.environ['DJANGO_MEDIA_URL']

if SITE_NAME == 'live':
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

TEMPLATE_DEBUG = DEBUG

SERVER_EMAIL = 'alerts@trapeze.com'

DEFAULT_HEADERS_EMAIL = {
    'From': DEFAULT_FROM_EMAIL,
    'Sender': DEFAULT_FROM_EMAIL,
}

# SES Email
EMAIL_BACKEND = 'django_ses.SESBackend' # Should other options be here too? See below
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

# S3 Storage for static & media
DEFAULT_FILE_STORAGE = 'utils.storage_backends.MediaS3Storage'
STATICFILES_STORAGE = 'utils.storage_backends.StaticS3Storage'
#THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

# Used by SES and Storages
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'  # Detect if client modified cookie via key
DEBUG_TOOLBAR_PATCH_SETTINGS = False # Required for toolbar not to adjust your settings, by default same as debug

# Misc data that may have to be set

#GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', None)

#FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', '')
#FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET', '')

#RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
#RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')

# if 'SENTRY_DSN' in os.environ:
#     RAVEN_CONFIG = {
#        'dsn': os.environ.get('SENTRY_DSN')
#     }

