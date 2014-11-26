#
# Dedicated to Djoume Salvetti
#

import fnmatch
from optparse import make_option
import os
import re
import sys

from django.core.management.base import BaseCommand, CommandError

from trapeze import settings as trapeze_settings
from trapeze.utils import spawn


PEP8_ARGS = ['--repeat', '--ignore', 'E501']

PYFLAKES_IMPORT_STAR_SEARCH = re.compile("(.+used; unable to detect undefined names\n?)")
CHECKSTYLE_IGNORE_SEARCH = re.compile('#.*checkstyle-ignore')
PYTHON_FILE_EXTENSIONS_FNMATCH = ['*.py', '*.py.ex']
IGNORE_FNMATCH = ['*manage.py', '*/migrations/*', '*media/files*', '*served/*']


def run_internal_checks(filename, contents, ignored_lines=None):
    # Trapeze specific checks
    # TODO: Handle ignored_lines at some point

    warnings = []

    def warn(s):
        warnings.append('%s: %s' % (filename, s))

    if len(contents) > 0:
        if contents[-1] != '\n':
            warn("no newline at end of file")

    if filename.endswith('models.py'):
        # TODO
        pass

    return '\n'.join(warnings).strip()


def run_pyflakes(filename, ignored_lines=None):
    old_pythonpath = os.environ.get('PYTHONPATH', None)
    os.environ['PYTHONPATH'] = trapeze_settings.PYFLAKES_MODULE_PATH
    output = spawn([trapeze_settings.PYFLAKES_BIN_PATH, filename])
    if old_pythonpath:
        os.environ['PYTHONPATH'] = old_pythonpath

    # Allow import *
    output = PYFLAKES_IMPORT_STAR_SEARCH.sub('', output)
    return filter_ignored_lines(output, ignored_lines)


def run_pep8(filename, ignored_lines=None):
    cmd_and_args = [trapeze_settings.PEP8_BIN_PATH]
    cmd_and_args.extend(PEP8_ARGS)
    cmd_and_args.append(filename)
    output = spawn(cmd_and_args)

    return filter_ignored_lines(output, ignored_lines)


def filter_ignored_lines(output, ignored_lines):
    # Filter output lines where lines are of the form
    #   <filename>:<line_number>:<rest...>
    if ignored_lines:
        new_output = []
        for line in output.splitlines():
            filename, line_number, rest = line.split(':', 2)
            if int(line_number) not in ignored_lines:
                new_output.append(line)

        return '\n'.join(new_output)
    else:
        return output


def get_ignored_line_numbers(contents):
    return [num for num, line in enumerate(contents.splitlines(), 1)
            if CHECKSTYLE_IGNORE_SEARCH.search(line)]


def checkstyle(filename, verbosity_level=1, with_pep8=True,
               with_pyflakes=True, with_internal_checks=True):
    warnings = []

    def warn(s):
        warnings.append(s)

    if not with_pep8 and not with_pyflakes and not with_internal_checks:
        warn("%s: no checks selected" % filename)

    contents = open(filename).read()
    ignored_lines = get_ignored_line_numbers(contents)

    pep8_out = run_pep8(filename, ignored_lines) if with_pep8 else ''
    pyflakes_out = run_pyflakes(filename, ignored_lines) if with_pyflakes else ''
    internal_checks_out = run_internal_checks(filename, contents, ignored_lines) if with_internal_checks else ''

    if pep8_out or pyflakes_out or internal_checks_out:
        if verbosity_level <= 0:
            warn("%s contains style violations" % filename)
        else:
            warn('%s %s %s' % ('*' * 3, filename, '*' * (65 - len(filename))))
            if pep8_out:
                warn("---> pep8")
                warn(pep8_out)
            if pyflakes_out:
                warn("---> pyflakes")
                warn(pyflakes_out)
            if internal_checks_out:
                warn("---> trapeze")
                warn(internal_checks_out)
            warn('')  # newline

    return '\n'.join(warnings).strip()


def is_python_file(filename, match=PYTHON_FILE_EXTENSIONS_FNMATCH, ignore=IGNORE_FNMATCH):
    return not any(fnmatch.fnmatch(filename, fnm) for fnm in ignore) and \
           any(fnmatch.fnmatch(filename, fnm) for fnm in match)


def walk_dir_for_python_files(directory, match=PYTHON_FILE_EXTENSIONS_FNMATCH, ignore=IGNORE_FNMATCH):
    for root, dirs, files in os.walk(directory):
        for f in files:
            f = os.path.join(root, f)
            if is_python_file(f, match, ignore):
                # Strip out ./ from filename
                yield f[2:] if f.startswith('./') else f


def walk_vcs_modified_python_files(match=PYTHON_FILE_EXTENSIONS_FNMATCH, ignore=IGNORE_FNMATCH):
    if os.path.exists('.svn'):
        svn_modified_re = re.compile(r'^(?:A|M)\s+(.*)$')
        # if this is A or M in svn status, run check_style() on it
        for svn_status_line in spawn(['svn', 'status']).splitlines():
            search = svn_modified_re.search(svn_status_line)
            if search:
                f = search.group(1)
                if is_python_file(f, match, ignore):
                    yield f


class Command(BaseCommand):
    args = '[<file1.py> <file2.py> <dirname> ...]'
    help = 'Check your python files for stylistic errors'

    option_list = BaseCommand.option_list + (
        # TODO: add support for git with -m (not just svn)
        make_option("-m", "--modified", action="store_true", dest="check_vcs",
                    default=False, help="Check modified or added files in local copy (svn only)"),
        make_option("-i", "--ignore", action="append", dest="ignore_files",
                    default=[], help="Unix style filename matches ignore (ie, *test.py)"),
        make_option("--without-pyflakes", action="store_false", dest="with_pyflakes",
                    default=True, help="Run without pyflakes checks"),
        make_option("--without-pep8", action="store_false", dest="with_pep8",
                    default=True, help="Run without pep8 checks"),
        make_option("--without-internal-checks", action="store_false", dest="with_internal_checks",
                    default=True, help="Run without Trapeze internal checks"),
    )

    def do_checkstyle(self, filename):
        output = checkstyle(
            filename,
            verbosity_level=self.verbosity,
            with_pep8=self.with_pep8,
            with_pyflakes=self.with_pyflakes,
            with_internal_checks=self.with_internal_checks,
        )

        if output:
            print output
            self.return_code = 1
        elif self.verbosity >= 2:
            print '%s: clean' % filename

    def do_checkstyle_dir(self, dirname):
        for f in walk_dir_for_python_files(dirname, ignore=self.fnmatch_to_ignore):
            self.do_checkstyle(f)

    def do_checkstyle_vcs(self):
        for f in walk_vcs_modified_python_files(ignore=self.fnmatch_to_ignore):
            self.do_checkstyle(f)

    def handle(self, *args, **options):
        self.fnmatch_to_ignore = options['ignore_files']
        self.fnmatch_to_ignore.extend(IGNORE_FNMATCH)
        self.verbosity = int(options['verbosity'])

        # Set self.with_* flags
        for k, v in options.iteritems():
            if k.startswith('with_'):
                setattr(self, k, v)

        self.return_code = 0

        if options['check_vcs']:
            self.do_checkstyle_vcs()
        elif args:
            for arg in args:
                if os.path.isfile(arg):
                    self.do_checkstyle(arg)
                elif os.path.isdir(arg):
                    self.do_checkstyle_dir(arg)
                else:
                    raise CommandError('Not a file or directory: %s' % arg)
        else:
            self.do_checkstyle_dir('.')

        sys.exit(self.return_code)
