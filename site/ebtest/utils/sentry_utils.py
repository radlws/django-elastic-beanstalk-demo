from django.conf import settings

from raven.contrib.django.raven_compat.models import client


class SentryTagMiddleware(object):

    def process_request(self, request):
        client.tags_context({
            'release': settings.RELEASE,
            # add any additional tags here
        })
