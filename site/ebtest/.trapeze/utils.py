import re
import os
import subprocess

from django.utils.translation import ugettext as _
from django.conf import settings as global_settings

from trapeze.exceptions import InvalidReleaseNameError


def spawn(cmd_and_args):
    comm = subprocess.Popen(cmd_and_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    stdout, stderr = comm[0].strip(), comm[1].strip()

    # Separate the two by a linebreak
    if stderr and stdout:
        return "%s\n%s" % (stdout, stderr)

    return "%s%s" % (stdout, stderr)


def split_release_name(full_release_name):
    """
    Breaks up the pieces of the release name, number and quality.
    """
    pieces = full_release_name.rsplit('-', 2)
    if len(pieces) < 2:
        raise InvalidReleaseNameError(_('The release name "%s" is not valid '
            '(it does not have a dash in it).') % full_release_name)

    results = {
        'name': pieces[0],
        'number': [],
        'quality': 'STABLE',
    }

    for piece in pieces[1:]:
        split = split_version_string(piece)
        if split:
            results['number'] += split['number']
            results['quality'] = split['quality']
        else:
            results['name'] += '-' + piece

    return results


def split_version_string(version_string):
    results = split_trapeze_style_version(version_string)
    if results:
        return results

    results = split_date_style_version(version_string)
    if results:
        return results

    results = split_revision_style_version(version_string)
    if results:
        return results

    results = split_numbered_style_version(version_string)
    if results:
        return results

    return None


def split_trapeze_style_version(version_string):
    results = {}
    trapeze_style = '(\d+)\.(\d+)\.(\d+)([a-zA-Z]+)'  # (eg. 1.2.3ALPHA)
    matches = re.search(trapeze_style, version_string)
    if matches:
        results['number'] = [matches.group(1), matches.group(2), matches.group(3)]
        results['quality'] = matches.group(4)
        return results
    return None


def split_numbered_style_version(version_string):
    results = {'number': [], 'quality': 'STABLE'}
    for piece in version_string.split('.'):
        try:
            int(piece)
        except ValueError:
            return None
        results['number'] += [piece]

    if not results['number']:
        return None
    return results


def split_date_style_version(version_string):
    results = {}
    date_style = '(2\d{7})'  # (eg. 20110604)
    matches = re.search(date_style, version_string)
    if matches:
        results['number'] = [matches.group(1)]
        results['quality'] = 'STABLE'
        return results
    return None


def split_revision_style_version(version_string):
    results = {}
    revision_style = '(r)(\d+)'  # (eg. r1738)
    matches = re.search(revision_style, version_string)
    if matches:
        results['number'] = [matches.group(1), matches.group(2)]
        results['quality'] = 'STABLE'
        return results
    return None


def compare_tags(tag1, tag2):
    """
    Returns 1 if tag1 is greater tag2, 0 if tag1 is equal to tag2, -1 otherwise.
    """
    tag1_pieces = split_release_name(tag1)
    tag2_pieces = split_release_name(tag2)

    if tag1_pieces['number'] == tag2_pieces['number']:
        quality_values = {'ALPHA': 0, 'BETA': 1, 'RC': 2, 'FINAL': 3, 'STABLE': 3}

        tag1_val = quality_values[tag1_pieces['quality'].upper()]
        tag2_val = quality_values[tag2_pieces['quality'].upper()]
        if tag1_val > tag2_val:
            return 1
        elif tag1_val == tag2_val:
            return 0
        else:
            return -1

    for i in range(len(tag1_pieces['number'])):
        tag1_val = tag1_pieces['number'][i]
        tag2_val = tag2_pieces['number'][i]

        if tag1_val == tag2_val == 'r':
            continue
        else:
            tag1_val = int(tag1_val)
            tag2_val = int(tag2_val)
        if tag1_val > tag2_val:
            return 1
        elif tag1_val < tag2_val:
            return -1

    return -1


def run_sql_command(sql, db_name=None):
    db_name = db_name or global_settings.DATABASES['default']['NAME']
    # Wraps the given SQL statement so that it can be piped into psql.
    # Escapes for the echo statement to handle quotes.
    command = """sudo su postgres -c "echo \\\"%(sql)s\\\" | psql %(db_name)s" """ % {
            'sql': sql,
            'db_name': db_name or '',
        }
    os.system(command) 
