"""
Module for common test stuff.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.test.utils import patch_logger


def no_request_warning():
    """Patch django.request logger to ignore warnings."""
    return patch_logger('django.request', 'warning', log_kwargs=False)
