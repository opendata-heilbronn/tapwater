"""
URL Configuration for water project.

The `url_patterns` as list for routes including views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.shortcuts import render_to_response
from django.template import RequestContext

# vars for different areas
LOGIN_AREA = "login"
USERS_AREA = "users"
ADMIN_AREA = "admin"

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    url(r'^', include('wasser.tapwater.urls')),
    url(r'^admin/', include('wasser.administration.urls')),
    url(r'^login/', include('wasser.login.urls')),
    url(r'^users/', include('wasser.users.urls')),
)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_URL)

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)


def handler404(request):
    """Handler for 404 errors."""
    response = render_to_response('404.html', {}, RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    """Handler for 500 errors."""
    response = render_to_response('500.html', {}, RequestContext(request))
    response.status_code = 500
    return response
