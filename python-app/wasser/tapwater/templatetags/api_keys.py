"""
User tags models.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""
from django import template
from wasser.settings import USE_GOOGLE_API, GOOGLE_GEO_API_KEY, \
    HERE_MAPS_GEO_APP_CODE, HERE_MAPS_GEO_APP_ID, GOOGLE_JAVASCRIPT_API_KEY

register = template.Library()


@register.simple_tag
def get_google_geo_api_key():
    """Get the geo api key."""
    return GOOGLE_GEO_API_KEY


@register.simple_tag
def get_google_api():
    """Return the value if its the free version or payed."""
    return USE_GOOGLE_API


@register.simple_tag
def get_here_maps_geo_app_id():
    """Return here maps geo api id."""
    return HERE_MAPS_GEO_APP_ID


@register.simple_tag
def get_here_maps_geo_app_code():
    """Return here maps geo api code."""
    return HERE_MAPS_GEO_APP_CODE


@register.simple_tag
def get_google_javascript_api_key():
    """Get the google javascript api key."""
    return GOOGLE_JAVASCRIPT_API_KEY
