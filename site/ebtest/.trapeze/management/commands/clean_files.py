import fnmatch
from optparse import make_option
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import models

# Deprecated?

class Command(BaseCommand):
    help = 'Remove media/files not referenced in the database.'

    option_list = BaseCommand.option_list + (
        make_option("-f", "--force", action="store_true", dest="force_delete",
                    default=False, help="Force deletion of media/files without prompting user."),
        make_option("-k", "--keep", action="store_true", dest="keep_files",
                    default=False, help="Keep media/files not referenced in the db. A dry run.")
    )

    def handle(self, **options):
        keep_files = options['keep_files']
        force_delete = options['force_delete']
        verbosity = int(options['verbosity'])

        # Warn of destructive operation
        if not any((force_delete, keep_files)):
            if not raw_input("Remove all media/files not referenced in the db (y/n)? ").strip().lower().startswith('y'):
                raise CommandError("User aborted.")

        # Make absolute, follow sym links, and normalize MEDIA_ROOT
        media_files_root = os.path.normpath(os.path.realpath(os.path.abspath(settings.MEDIA_ROOT)))

        # Start all off with all files as untracked
        files_untracked = []
        for basedir, dirs, files in os.walk(media_files_root):
            if fnmatch.fnmatch(basedir, '*/.svn*'):
                continue

            for f in files:
                files_untracked.append(os.path.join(basedir, f))

        # Through all models, eleminating files from untracked_media_files list
        files_in_db_not_found = 0
        files_in_db_found = 0

        for model in models.get_models():
            # Get file fields on this model (if any)
            file_field_names = [f.name for f in model._meta.fields if isinstance(f, models.FileField)]

            if file_field_names:
                # Go through all entries in db
                for instance in model.objects.all():
                    for file_field_name in file_field_names:
                        file_field = getattr(instance, file_field_name)

                        if file_field:
                            file_path = file_field.path

                            try:
                                files_untracked.remove(file_path)
                                files_in_db_found += 1
                            except ValueError:
                                files_in_db_not_found += 1

        # Remove the files
        if not keep_files:
            for f in files_untracked:
                os.remove(f)

        if verbosity >= 1:
            if files_untracked:
                print "Untracked files..."
                for f in files_untracked:
                    print f
                print

        print "          Files referenced in db: %d" % files_in_db_found
        print "Files referenced in db not found: %d" % files_in_db_not_found
        print "      Files not referenced in db: %d (%s)" % (
            len(files_untracked),
            'kept' if keep_files else 'deleted',
        )
