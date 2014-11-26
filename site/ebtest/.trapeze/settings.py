import os

from django.conf import settings

# Set this to False to disable auto-generation of checkstyle tests for each
# Python (.py/.py.ex) file in your project.
CHECKSTYLE_TESTS_ENABLED = getattr(settings, 'CHECKSTYLE_TESTS_ENABLED', True)

# A list that includes 'pep8', 'pyflakes', and/or 'internal_checks'
# to enable certain of the checkstyle checks. See the the source to
# trapeze/management/commands/checkstyle.py for more detailed info.
# Use this, for example, to disable pep8 checks but run pyflakes
CHECKSTYLE_TESTS_CHECKS = getattr(settings, 'CHECKSTYLE_TESTS_CHECKS',
    ['pep8', 'pyflakes', 'internal_checks'],
)

# A list of exact filenames relative to PROJECT_PATH to additionally check.
CHECKSTYLE_TESTS_ADDITIONAL_FILES = getattr(settings, 'CHECKSTYLE_TESTS_ADDITIONAL_FILES', [])

# A list of exact filenames relative to PROJECT_PATH to not generate tests
# for and avoid checking.
CHECKSTYLE_TESTS_BLACKLIST_FILES = getattr(settings, 'CHECKSTYLE_TESTS_BLACKLIST_FILES', [])


PATH_TO_DEVDATA = getattr(settings, 'PATH_TO_DEVDATA', '../../devdata/')

SRC_FOLDER = getattr(settings, 'SRC_FOLDER', '../src/')

LIB_FOLDER = getattr(settings, 'SRC_FOLDER', '../lib/')

REUSABLE_APP_SVN_PATH = getattr(settings, 'REUSABLE_APP_SVN_PATH',
    'https://office.trapeze.com/svn/DjangoApps/',
)

EXCLUDE_FROM_UPGRADES = getattr(settings, 'EXCLUDE_FROM_UPGRADES', [])

APP_NAMES_TO_PACKAGE = getattr(settings, 'APP_NAMES_TO_PACKAGE', {
    'absolute_media_url': 'django-absolute-media-url',
    'django_extensions': 'django-command-extensions',
})

PYFLAKES_MODULE_PATH = getattr(settings, 'PYFLAKES_MODULE_PATH',
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libs', 'pyflakes-0.5.0'),
)

PYFLAKES_BIN_PATH = getattr(settings, 'PYFLAKES_BIN_PATH',
    os.path.join(PYFLAKES_MODULE_PATH, 'bin', 'pyflakes'),
)

PEP8_BIN_PATH = getattr(settings, 'PEP8_BIN_PATH',
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libs', 'pep8-1.0.1', 'pep8.py'),
)

# added --delete-excluded, http://serverfault.com/questions/573392/rsync-cannot-delete-non-empty-directory-errors-even-with-force-option
RSYNC_OPTIONS = '--recursive --links --times --omit-dir-times --verbose --delete --delete-excluded --exclude=.svn --exclude="*_q85*"'
