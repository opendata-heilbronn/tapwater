"""
URL Configuration for water project.

The `url_patterns` as list for routes including views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.conf.urls import url
from wasser.login.utilities import login_required

from . import views

urlpatterns = [
    url(r'^' + '$',
        login_required(views.users_index),
        name='users_index'),
    url(r'^' + 'request/token/new/$',
        views.send_token_for_one_user,
        name='send_token_for_one_user'),
    url(r'^' + 'measurement/insert/$',
        login_required(views.insert_measurement),
        name='insert_measurement'),
    url(r'^' + 'measurements/user/show/$',
        login_required(views.show_measurements_user),
        name='show_measurements_user'),
    url(r'^' + 'registration/$',
        views.registration,
        name='registration'),
    url(r'^' + 'logout/$',
        views.users_logout,
        name='users_logout'),
]
