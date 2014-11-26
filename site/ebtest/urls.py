from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, patterns
from django.contrib import admin
from django.template.response import TemplateResponse

admin.autodiscover()


urlpatterns = patterns('',
    (r'', include('home.urls')),
    (r'^cmsadmin/', include(admin.site.urls)),
    # (r'^foo-app/', include('foo_app.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', TemplateResponse, {'template': '404.html'}))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add custom error views. More here: https://docs.djangoproject.com/en/dev/topics/http/views/
# handler404 = "home.views.page_not_found_view", uses default location
# handler400 = 'home.views.bad_request_view'
# handler500 = "home.views.views.server_error_view"
# handler403 = 'home.views.permission_denied_view'

# For prod emulation. Enable static for runserver with DEBUG False. if DEBUG, it is  served automatically
#from django.conf import settings
#if settings.DEBUG is False and settings.SITE_NAME not in settings.PRODUCTION_SITES:
#    urlpatterns += patterns('',
#        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#    )
