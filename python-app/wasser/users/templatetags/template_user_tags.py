"""
User tags models.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""
from django import template
from django.shortcuts import get_object_or_404
from wasser.administration.models import TapwaterUser

register = template.Library()


@register.simple_tag
def get_username_from_userid(user_id):
    """Get the username of the current user by id."""
    user = get_object_or_404(TapwaterUser, id=user_id)
    return user.firstname
