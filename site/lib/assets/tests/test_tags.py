from django.test import TestCase
from django.template import Template, Context
from django.test.utils import override_settings
from django.utils import translation


def render(template_string, context_dict=None):
    """
    A shortcut for testing template output. Taken from django_compressor
    https://github.com/jezdez/django_compressor/blob/develop/compressor/tests/test_templatetags.py#L16
    """
    if context_dict is None:
        context_dict = {}
    c = Context(context_dict)
    t = Template(template_string)
    return t.render(c).strip()


@override_settings(ASSETS_DEV=True)
class AssetsDevTestCase(TestCase):

    def test_less_tag(self):
        template = u"""{% load assets %} {% use_asset "less" "core" %}"""
        out = u'<link href="/static/css/base.css" media="screen" rel="stylesheet" />\n' \
            '<link href="/static/subfolder/css/sub.css" media="screen" rel="stylesheet" />'

        self.assertEqual(out, render(template))

    def test_css_tag(self):
        template = u"""{% load assets %} {% use_asset "css" "page" %}"""
        out = u'<link href="/static/css/page.css" rel="stylesheet" />'
        self.assertEqual(out, render(template))

    def test_js_tag(self):
        template = u"""{% load assets %} {% use_asset "js" "core" %}"""
        out = u'<script src="/static/js/core.js"></script>'
        self.assertEqual(out, render(template))

    def test_i18n_tag(self):
        template = u"""{% load assets %} {% use_i18n_asset "js" "test" %}"""
        out = u'<script src="/static/js/test-en.js"></script>'

        with translation.override('en'):
            self.assertEqual(out, render(template))

        out = u'<script src="/static/js/test-fr.js"></script>'

        with translation.override('fr'):
            self.assertEqual(out, render(template))

    def test_namespaced_tag(self):
        template = u"""{% load assets %} {% use_asset "js" "test_app:core" %}"""
        out = u'<script src="/static/js/core.js"></script>'

        self.assertEqual(out, render(template))


@override_settings(ASSETS_DEV=False)
class AssetsLiveTestCase(TestCase):

    def test_less_tag(self):
        template = u"""{% load assets %} {% use_asset "less" "core" %}"""
        out = u'<link href="/static/compiled/css/core.min.css" media="screen" rel="stylesheet" />'
        self.assertEqual(out, render(template))

    def test_css_tag(self):
        template = u"""{% load assets %} {% use_asset "css" "page" %}"""
        out = u'<link href="/static/compiled/css/page.min.css" rel="stylesheet" />'
        self.assertEqual(out, render(template))

    def test_js_tag(self):
        template = u"""{% load assets %} {% use_asset "js" "core" %}"""
        out = u'<script src="/static/compiled/js/core.min.js"></script>'
        self.assertEqual(out, render(template))

    def test_i18n_tag(self):
        template = u"""{% load assets %} {% use_i18n_asset "js" "test" %}"""
        out = u'<script src="/static/compiled/js/test-en.min.js"></script>'

        with translation.override('en'):
            self.assertEqual(out, render(template))

        out = u'<script src="/static/compiled/js/test-fr.min.js"></script>'

        with translation.override('fr'):
            self.assertEqual(out, render(template))

    def test_namespaced_tag(self):
        template = u"""{% load assets %} {% use_asset "js" "test_app:core" %}"""
        out = u'<script src="/static/compiled/js/core.min.js"></script>'

        self.assertEqual(out, render(template))


@override_settings(ASSETS_SERVE_LESS=True, ASSETS_DEV=True)
class AssetsServeLessTestCase(TestCase):

    def test_less_tag(self):
        template = u"""{% load assets %} {% use_asset "less" "core" %}"""
        out = u'<link href="/static/less/base.less" media="screen" rel="stylesheet/less" />\n' \
            '<link href="/static/subfolder/less/sub.less" media="screen" rel="stylesheet/less" />'
        self.assertEqual(out, render(template))
