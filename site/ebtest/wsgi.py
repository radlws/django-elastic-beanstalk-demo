import os
import sys


#UNCOMMENT for beanstalk prod use, COMMENT the default DJANGO_SETTINGS_MODULE below
from os.path import abspath, dirname
from sys import path
SITE_ROOT = dirname(abspath(__file__))
path.append(SITE_ROOT)
LIB = abspath(os.path.join(SITE_ROOT, '../lib'))
path.append(LIB)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_prod")

#COMMENT if using beanstalk configuration above
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Django 1.7, works for 1.6 as well
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


