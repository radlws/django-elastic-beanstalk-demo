import os
import django

DEBUG = True

TEST_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests')

if django.VERSION[:2] >= (1, 3):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASE_ENGINE = 'sqlite3'

LANGUAGE_CODE = 'en'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('fr', gettext('French')),
)


INSTALLED_APPS = [
    'assets',

    'assets.tests.test_app',
]

TEMPLATE_DIRS = (
    os.path.join(TEST_DIR, 'templates'),
)

STATIC_URL = '/static/'

TEST_RUNNER = 'discover_runner.DiscoverRunner'

SECRET_KEY = "iufoj=mibkpdz*%bob952x(%49rqgv8gg45k36kjcg76&-y5=!"

ROOT_URLCONF = 'tests.urls'

ASSETS_CONFIG = os.path.join(TEST_DIR, 'assets.json')
ASSETS_CSS_DEST = 'css/'
ASSETS_SERVE_LESS = False
