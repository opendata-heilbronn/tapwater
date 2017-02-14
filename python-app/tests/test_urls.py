"""
test for tapwater views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.test import TestCase, RequestFactory
from django.shortcuts import reverse

from wasser.urls import handler500


class TapwaterViewsTest(TestCase):
    """Unit test class for tapwater views."""

    def setUp(self):
        """Setup the unit test."""
        self.factory = RequestFactory()

    def test_server_error_handler(self):
        """Test server error."""
        request = self.factory.get(reverse("admin_index"))
        response = handler500(request)
        self.assertEqual(response.status_code, 500)
