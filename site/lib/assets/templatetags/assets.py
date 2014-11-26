import json
import os
import re

from django.conf import settings
from django import template
from django.contrib.admin.templatetags.admin_static import static
from django.core.exceptions import ImproperlyConfigured
from django.forms.util import flatatt
from django.utils import translation
from django.utils.importlib import import_module

LESS_PATH_RE = re.compile(r'(less(?=/))|((?<=\.)less)')

ASSETS_CONFIG = getattr(settings, 'ASSETS_CONFIG', 'assets.json')
ASSETS = {'__base__': {}}

try:
    with open(ASSETS_CONFIG) as f:
        ASSETS['__base__'] = json.loads(f.read())

except IOError:
    raise ImproperlyConfigured("Asset configuration file %s not found" %
            ASSETS_CONFIG)


def load_assets_from_apps(asset_cache):
    for app in settings.INSTALLED_APPS:
        try:
            mod = import_module(app)
        except ImportError:
            continue

        asset_file = os.path.join(os.path.dirname(mod.__file__), 'assets.json')

        if os.path.exists(asset_file):
            app_name = app.split('.')[-1]
            with open(asset_file) as f:
                asset_cache[app_name] = json.loads(f.read())

load_assets_from_apps(ASSETS)

register = template.Library()


class AssetNode(template.Node):
    def __init__(self, key, name, version=None, localized=False):
        self.key = key
        self.name = name
        self.localized = localized

        self.version = version

        self.asset_group = None  # Set in render()

    def get_dev(self):
        # Fetch development setting on demand
        return getattr(settings, 'ASSETS_DEV', False)

    def get_path(self, path):
        if self.get_dev():
            return static(path)
        else:
            return static(self.asset_group['dest'])

    def get_css_path(self, less_path):
        return LESS_PATH_RE.sub('css', less_path)

    def get_version_tag(self):
        if self.version:
            return "?v={0}".format(self.version).replace('"', '')
        else:
            return ''

    def get_js_tag(self, path):

        return '<script src="{0}{1}"{2}></script>'.format(
            self.get_path(path),
            self.get_version_tag(),
            flatatt(self.asset_group.get('attrs', {})),
        )

    def get_css_tag(self, path):
        attrs = self.asset_group.get('attrs', {})

        if not attrs.get('rel'):
            attrs['rel'] = 'stylesheet'
        return '<link href="{0}{1}"{2} />'.format(
            self.get_path(path),
            self.get_version_tag(),
            flatatt(attrs),
        )

    def get_less_tag(self, path):
        attrs = self.asset_group.get('attrs', {})
        css_path = path

        if getattr(settings, 'ASSETS_SERVE_LESS', False) and self.get_dev():
            attrs['rel'] = 'stylesheet/less'

        else:
            css_path = self.get_css_path(path)

            if 'rel' not in attrs:
                attrs['rel'] = 'stylesheet'

        return '<link href="{0}{1}"{2} />'.format(self.get_path(css_path), self.get_version_tag(), flatatt(attrs))

    def render(self, context):
        asset_name = template.Variable(self.name).resolve(context)

        if self.localized:
            asset_name = "%s_%s" % (asset_name, translation.get_language()[:2])

        if ':' in asset_name:
            namespace, asset_name = asset_name.split(':', 1)
        else:
            namespace = '__base__'

        try:
            self.asset_group = ASSETS[namespace][self.key][asset_name]
        except KeyError:
            raise ImproperlyConfigured('Invalid asset group: %s %s:%s' % (self.key,
                namespace, asset_name))

        output = []
        if self.get_dev():
            for asset in self.asset_group['src']:
                output.append(getattr(self, 'get_%s_tag' % self.key)(asset))
        else:
            output.append(getattr(self, 'get_%s_tag' % self.key)(self.asset_group['dest']))
        return '\n'.join(output)


def make_args(parser, token):

    split_token = token.split_contents()
    try:
        if len(split_token) == 3:  # if not version included
            tag_name, key, name = split_token
            return (key[1:-1], name)
        elif len(split_token) == 4:  # 4 args, meaning name of tag, key, name & version
            tag_name, key, name, version = split_token
            return (key[1:-1], name, version)
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r requires exactly two arguments: the key of an asset type and'
            ' asset group in the %s setting' % (token.split_contents()[0], ASSETS_CONFIG)
        )


@register.tag
def use_asset(parser, token):
    args = make_args(parser, token)
    return AssetNode(*args)


@register.tag
def use_i18n_asset(parser, token):
    args = make_args(parser, token)
    return AssetNode(localized=True, *args)
