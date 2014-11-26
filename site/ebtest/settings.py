# Django project settings file
# This file should be part of the svn repository of the project and should not
# contains any site-specific information.
# site-specific information (database name/login/password for example) should be
# in the settings_local.py file and should not be added to the svn repository

import os

# By default urllib, urllib2, and the like have no timeout which can cause
# some apache processes to hang until they are forced kill.
# See http://ticket.trapeze.com/app/item/D001003-44/ or
# http://ticket.trapeze.com/app/item/D625021-218/
# Before python 2.6, the only way to cause them to time out is by setting
# the default timeout on the global socket
import socket
socket.setdefaulttimeout(5)

ROOT_URLCONF = 'urls'

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

with open(os.path.join(PROJECT_PATH, '../RELEASES')) as rel_file:
    RELEASE = rel_file.readline().strip()

SITE_ID = 1

USE_I18N = True

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Toronto'

# https://docs.djangoproject.com/en/dev/releases/1.6/#new-test-runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'  # Defines default test runner for django 1.7

# Allows you to include globs of IP addresses in INTERNAL_IPS.
from fnmatch import fnmatch


class IPList(list):
    def __contains__(self, key):
        for elt in self:
            if fnmatch(key, elt):
                return True
        return False

INTERNAL_IPS = IPList(['127.0.0.1', '192.168.1.*', '192.168.111.*', '10.10.*'])

gettext = lambda s: s
LANGUAGES = (('en', gettext('English')),)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'utils.sentry_utils.SentryTagMiddleware',  # (optional)
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# The folders that contain files that are served statically (ie. NOT served by Django)
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'served/media/')  # Uploaded content
STATIC_ROOT = os.path.join(PROJECT_PATH, 'served/static/')  # Static files: css, js, images, etc.

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/'),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, 'locale/'),
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static/'),
)

FILE_UPLOAD_PERMISSIONS = 0664  # Filer / easy thumbs permissions
#Easy Thumbnails, debug production, otherwise fails silently
#THUMBNAIL_DEBUG = True 

INSTALLED_APPS = (
    # Django contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Reusable
    'assets',
    #'raven.contrib.django.raven_compat', # optional
    'trapeze',

    # Project-specific
    'home',
)

ASSETS_CONFIG = os.path.join(PROJECT_PATH, 'assets.json')
ASSETS_CSS_DEST = 'css/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {  # send email on error 500
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ADMINS = (
    ('Django Alerts', 'alerts@support.trapeze.com'),   #TODO: will need to fix to use unioncreative
)

MANAGERS = ADMINS

# import local settings overriding the defaults
from settings_local import *

TEMPLATE_DEBUG = DEBUG

SERVER_EMAIL = DEFAULT_FROM_EMAIL

DEFAULT_HEADERS_EMAIL = {
    'From': DEFAULT_FROM_EMAIL,
    'Sender': DEFAULT_FROM_EMAIL,
}

#GRAPPELLI_ADMIN_TITLE = 'Site Admin &nbsp; <a href="/">Back to Site</a>'
#GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

FILEBROWSER_OVERWRITE_EXISTING = False
#FILEBROWSER_DIRECTORY = 'uploads/'  # Set the Grappelli upload directory, /uploads is default
#VALID_IMAGES = [".jpg", ".png", ".gif"]  # Global wide variable for file uploads via filebrowser

# Create the default filebrowser direcctory
if not os.path.exists(os.path.join(MEDIA_ROOT, 'uploads')):
    os.makedirs(os.path.join(MEDIA_ROOT, 'uploads'))