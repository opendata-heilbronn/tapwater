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
    url(r'^$',
        views.index,
        name='index'),
    url(r'^' + 'ajax/location',
        views.load_tapwater_locations,
        name='load_tapwater_locations'),
    url(r'^' + 'show',
        views.show_tapwater_values,
        name='show_tapwater_values'),
    url(r'^' + 'autocomplete/cities',
        views.auto_complete_search_cities,
        name='autocomplete_tapwater_cities'),
]
