"""
URL Configuration for water project.

The `url_patterns` as list for routes including views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^' + '$',
        views.login_authority,
        name='login_authority'),
    url(r'^' + 'admin/$',
        views.login_admin,
        name='admin_login'),
    url(r'^' + 'failed/$',
        views.login_failed,
        name='user_login_failed'),
    url(r'^' + 'admin/failed$',
        views.admin_login_failed,
        name='admin_login_failed'),
]
