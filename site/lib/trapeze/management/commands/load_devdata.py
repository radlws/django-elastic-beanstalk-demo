import commands
import os

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from trapeze import settings as trapeze_settings
from trapeze.utils import run_sql_command


class Command(BaseCommand):
    help = 'Loads database and files from devdata'
    option_list = BaseCommand.option_list + (
        make_option('--path', action='store', dest='path', type='string',
            help='Path to devdata folder'),
    )

    def handle(self, **options):
        path = options.get('path') or trapeze_settings.PATH_TO_DEVDATA
        if not os.path.exists(path):
            self.stderr.write('Devdata path does not exist: %s\n' % path)
            return

        devdata_files = os.path.join(path, 'files/')
        media_files = settings.MEDIA_ROOT

        if not os.path.exists(media_files):
            self.stderr.write('Media files path does not exist: %s\n' % media_files)

        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        if "live" in db_name:
            response = raw_input('Looks like you are loading dev data on a live database.'
                ' Are you sure you want to do this?'
                '\nType "yes" to continue: '
            )
            if response != "yes":
                self.stdout.write('Exiting\n')
                return

        # Drop the database
        dropdb = 'sudo su postgres -c "dropdb %(db)s"' % \
            {
                'db': db_name,
            }
        self.stdout.write('Dropping database: %s\n' % db_name)
        status, output = commands.getstatusoutput(dropdb)

        # Create the database
        createdb = 'sudo su postgres -c "createdb -O %(user)s %(db)s"' % {
            'user': db_user,
            'db': db_name,
        }
        self.stdout.write('Creating database: %s\n' % db_name)
        status, output = commands.getstatusoutput(createdb)

        # Add spatial database support
        run_sql_command('CREATE EXTENSION postgis;')
        postgis_tables = [
            'spatial_ref_sys',
            'geometry_columns',
            'geography_columns',
        ]
        for table_name in postgis_tables:
            sql = 'ALTER TABLE %(table_name)s OWNER TO %(db_user)s;' % {
                        'table_name': table_name,
                        'db_user': db_user,
                    }
            run_sql_command(sql)

        # Load the database dump
        dump_sql = os.path.join(path, 'dump.sql')
        shell_load = './manage.py dbshell < %(dump_sql)s' % {'dump_sql': dump_sql}
        status, output = commands.getstatusoutput(shell_load)
        if status != 0:
            self.stderr.write(output + "\n")
            return
        else:
            self.stdout.write(output + "\n")

        if not os.path.exists(devdata_files):
            return

        # Rsync media files
        rsync_files = 'rsync %(options)s %(devdata_files)s %(media_files)s ' % {
            'devdata_files': devdata_files,
            'media_files': media_files,
            'options': trapeze_settings.RSYNC_OPTIONS,
        }
        status, output = commands.getstatusoutput(rsync_files)
        self.stdout.write(output)
        if status != 0:
            self.stderr.write(output + "\n")
            return
        else:
            self.stdout.write(output + "\n")

        status, output = commands.getstatusoutput('sudo chmod -R g+rws %s'.format(media_files))
        self.stdout.write(output)
        if status != 0:
            self.stderr.write(output + "\n")
            return
        else:
            self.stdout.write(output + "\n")