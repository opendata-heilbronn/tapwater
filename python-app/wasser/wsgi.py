"""
WSGI Config for water project.

See also: https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wasser.settings")

WSGI_APPLICATION = get_wsgi_application()
