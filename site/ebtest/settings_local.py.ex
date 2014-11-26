# Django project site specific settings
# All non site specific settings should go into the settings.py file
# Copy this file as settings_local.py and adjust it to your site.
# The settings_local.py contains only site specific information and should not
# be part of the svn repository of the project. It should be part of the
# hosting svn repository.

SITE_NAME = '<site_name>'

PRODUCTION_SITES = ['live', 'staging']

if SITE_NAME in PRODUCTION_SITES:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['.trapeze.com']  # TODO: Change on production

SECRET_KEY = '(xxq$%nk3o!4q_)xfwb88u3=^mk71n9&-i&qq=l@1h_6(6)-0i'  # TODO Change on production

DEFAULT_FROM_EMAIL = 'messenger@<hostname>'

# Uncomment on local development if debug is False.
# This will overwrite the common setting that points to the alert mailbox.
#ADMINS = (('Django Alerts', '<email>'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<project_name>_<site_name>',
        'USER': '<db_user>',
        'PASSWORD': '<db_password>',
        'HOST': '127.0.0.1',
        # 'PORT': 5433,  # Uncomment if using pgpool
        'OPTIONS': {
            'autocommit': True,
        },
    }
}

# Django needs to know the version number, otherwise it tries to make an
# initial connection to postgres before running management commands.
POSTGIS_VERSION = (2, 0, 1)


if SITE_NAME in PRODUCTION_SITES:
    STATIC_URL = '//<domain_name>/static/'
    MEDIA_URL = '//<domain_name>/media/'
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

if SITE_NAME in PRODUCTION_SITES:
    FILE_UPLOAD_TEMP_DIR = '/home/<project_name>team/<site_name>/tmp'

if SITE_NAME == 'live':
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

# Uncomment this if you want original assets
# ASSETS_DEV = True


# TODO Change on production
# RAVEN_CONFIG = {
#    'dsn': 'https://080256ce2e8549da9fc9db5b665e1a0a:063e6ca70f1a4380867b2826e86d05ef@app.getsentry.com/22320',
# }
