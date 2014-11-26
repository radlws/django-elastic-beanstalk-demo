import os
from subprocess import call

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Run all the tests (even the ones from reusable apps)'

    def handle(self, **options):
        for app in settings.INSTALLED_APPS:
            i = app.rfind('.')
            if i == -1:
                m, a = app, None
            else:
                m, a = app[:i], app[i + 1:]
            try:
                if a is None:
                    mod = __import__(m, {}, {}, [])
                else:
                    mod = getattr(__import__(m, {}, {}, [a]), a)
            except ImportError, e:
                raise CommandError('ImportError %s: %s\n' % (app, e.args[0]))

            if os.path.exists(os.path.join(os.path.dirname(mod.__file__),
                    'tests/settings.py')):
                self.stdout.write("Running tests for %s...\n" % app)
                call(['python', 'manage.py', 'test', 'tests', '--verbosity=0',
                    '--settings=%s.tests.settings' % app])

        self.stdout.write('Running remaining tests...\n')
        call(['python', 'manage.py', 'test', '--verbosity=1',
            '--settings=settings'])
