import os
import re

from django.test import TestCase

from trapeze.management.commands import checkstyle
from trapeze import settings as trapeze_settings
from trapeze.utils import compare_tags, split_release_name

"""
The following should be manually tested:

./manage.py get_app
./manage.py upgrade

"""


class UtilsTests(TestCase):
    def test_split_release_name_for_inhouse_app(self):
        result = split_release_name('some-app-1.2.3STABLE')
        self.assertEquals(result['name'], 'some-app')
        self.assertEquals(result['number'], ['1', '2', '3'])
        self.assertEquals(result['quality'], 'STABLE')

    def test_split_release_name_for_third_party_app(self):
        result = split_release_name('some-app-1.2.3')
        self.assertEquals(result['name'], 'some-app')
        self.assertEquals(result['number'], ['1', '2', '3'])
        self.assertEquals(result['quality'], 'STABLE')

        result = split_release_name('some-app-1.2.3-4.5.6ALPHA')
        self.assertEquals(result['name'], 'some-app')
        self.assertEquals(result['number'], ['1', '2', '3', '4', '5', '6'])
        self.assertEquals(result['quality'], 'ALPHA')

    def test_split_release_name_for_third_party_app_date_tagged(self):
        result = split_release_name('some-app-20091013')
        self.assertEquals(result['name'], 'some-app')
        self.assertEquals(result['number'], ['20091013'])
        self.assertEquals(result['quality'], 'STABLE')

        result = split_release_name('some-app-20091013-4.5.6ALPHA')
        self.assertEquals(result['name'], 'some-app')
        self.assertEquals(result['number'], ['20091013', '4', '5', '6'])
        self.assertEquals(result['quality'], 'ALPHA')

    def test_split_release_name_for_third_party_app_revision_tagged(self):
        result = split_release_name('someapp-r277')
        self.assertEquals(result['name'], 'someapp')
        self.assertEquals(result['number'], ['r', '277'])
        self.assertEquals(result['quality'], 'STABLE')

        result = split_release_name('someapp-r277-1.2.3ALPHA')
        self.assertEquals(result['name'], 'someapp')
        self.assertEquals(result['number'], ['r', '277', '1', '2', '3'])
        self.assertEquals(result['quality'], 'ALPHA')

    def test_split_release_name_for_third_pary_app_no_number(self):
        result = split_release_name('someapp-abcde')
        self.assertEquals(result['name'], 'someapp-abcde')
        self.assertEquals(result['number'], [])
        self.assertEquals(result['quality'], 'STABLE')

    def test_compare_tags_method(self):
        self.assertEquals(compare_tags('abc-xyz1-0.10.0ALPHA', 'abc-xyz1-0.9.0ALPHA'), 1)
        self.assertEquals(compare_tags('abc-0.5.11ALPHA', 'abc-0.5.10ALPHA'), 1)
        self.assertEquals(compare_tags('abc-2.0.1STABLE', 'abc-1.8.6ALPHA'), 1)
        self.assertEquals(compare_tags('abc-0.1.0ALPHA', 'abc-0.12.0ALPHA'), -1)
        self.assertEquals(compare_tags('abc-2.3.4RC', 'abc-2.3.4STABLE'), -1)
        self.assertEquals(compare_tags('abc-2.3.4RC', 'abc-2.3.4FINAL'), -1)
        self.assertEquals(compare_tags('abc-2.3.4STABLE', 'abc-2.3.4FINAL'), 0)

    def test_compare_tags_method_for_third_party_app(self):
        self.assertEquals(compare_tags('some-app-0.4.1-1.0.1STABLE', 'some-app-0.4.1-1.0.1STABLE'), 0)
        self.assertEquals(compare_tags('some-app-0.4.1-1.0.1STABLE', 'some-app-0.4.0-1.1.2STABLE'), 1)
        self.assertEquals(compare_tags('some-app-0.4.1-1.0.1STABLE', 'some-app-0.5.0-1.0.0ALPHA'), -1)
        self.assertEquals(compare_tags('some-app-0.4.1-1.0.1STABLE', 'some-app-0.5.0'), -1)

    def test_compare_tags_method_for_third_party_app_date_tagged(self):
        self.assertEquals(compare_tags('some-app-20110613-1.0.1STABLE', 'some-app-20110613-1.0.1STABLE'), 0)
        self.assertEquals(compare_tags('some-app-20110901-1.0.1STABLE', 'some-app-20110613-1.1.2STABLE'), 1)
        self.assertEquals(compare_tags('some-app-20110613-1.0.1STABLE', 'some-app-20110901-1.0.0ALPHA'), -1)
        self.assertEquals(compare_tags('some-app-20110613-1.0.1STABLE', 'some-app-20110901'), -1)

    def test_compare_tags_method_for_third_party_app_revision_tagged(self):
        self.assertEquals(compare_tags('some-app-r4393-1.0.1STABLE', 'some-app-r4393-1.0.1STABLE'), 0)
        self.assertEquals(compare_tags('some-app-r7839-1.0.1STABLE', 'some-app-r4393-1.1.2STABLE'), 1)
        self.assertEquals(compare_tags('some-app-r4393-1.0.1STABLE', 'some-app-r7839-1.0.0ALPHA'), -1)
        self.assertEquals(compare_tags('some-app-r4393-1.0.1STABLE', 'some-app-r7839'), -1)


class CheckstyleTests(TestCase):
    # Dynamically add tests to class if required. This is an empty TestCase
    # if CHECKSTYLE_TESTS_ENABLED = False
    if trapeze_settings.CHECKSTYLE_TESTS_ENABLED:
        def generate_checkstyle_tests_for_project(class_namespace):
            FUNC_NAME_SANITIZER = re.compile('[^a-zA-Z0-9_]')
            WHICH_CHECKS_TO_RUN_KWARGS = {
                'with_pep8': 'pep8' in trapeze_settings.CHECKSTYLE_TESTS_CHECKS,
                'with_pyflakes': 'pyflakes' in trapeze_settings.CHECKSTYLE_TESTS_CHECKS,
                'with_internal_checks': 'internal_checks' in trapeze_settings.CHECKSTYLE_TESTS_CHECKS,
            }

            def generate_checkstyle_test(filename):
                def checkstyle_test(self):
                    output = checkstyle.checkstyle(filename, **WHICH_CHECKS_TO_RUN_KWARGS)
                    if output:
                        formatted_output = "%s\n%s\n%s" % (
                            (' BEGIN CHECKSTYLE OUTPUT ').center(70, '#'),
                            output.strip(),
                            (' END CHECKSTYLE OUTPUT ').center(70, '#'),
                        )
                        self.fail("%s did not pass checkstyle\n\n%s" % (filename, formatted_output))

                checkstyle_test.__name__ = "test_checkstyle_on_%s" % (
                    FUNC_NAME_SANITIZER.sub('_', filename),
                )

                return checkstyle_test

            files_to_check = list(checkstyle.walk_dir_for_python_files('.')) \
                           + trapeze_settings.CHECKSTYLE_TESTS_ADDITIONAL_FILES

            for f in trapeze_settings.CHECKSTYLE_TESTS_ADDITIONAL_FILES:
                if not os.path.exists(f):
                    print "trapeze: %s in was supposed to be checked but does not exist" % f
                    files_to_check.remove(f)

            for f in trapeze_settings.CHECKSTYLE_TESTS_BLACKLIST_FILES:
                try:
                    files_to_check.remove(f)
                except ValueError:
                    print "trapeze: %s is blacklisted but was not to be checked" % f

            for f in files_to_check:
                test_func = generate_checkstyle_test(f)
                class_namespace[test_func.__name__] = test_func

        generate_checkstyle_tests_for_project(locals())

        # Remove this function from the class namespace
        del generate_checkstyle_tests_for_project
