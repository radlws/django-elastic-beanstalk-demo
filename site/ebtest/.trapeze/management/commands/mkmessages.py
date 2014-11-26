from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run makemessages with --extension=html,txt automatically.'

    def handle(self, *args, **options):
        options.update({'extensions': ['html,txt'], 'all': True})
        management.call_command('makemessages', *args, **options)
