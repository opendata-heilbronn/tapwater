"""
test for tapwater views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.test import TestCase
from django.urls import reverse


class TapwaterViewsTest(TestCase):
    """Unit test class for tapwater views."""

    fixtures = ['tests/fixtures/tapwater_fixture.json',
                'tests/fixtures/users_fixture.json',
                'tests/fixtures/administration_fixture.json']

    def setUp(self):
        """
        Set up unit test.

        :return:
        """
        self.xml_http_request = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_tapwater_main(self):
        """
        Test main page of tapwater.

        :return:
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_load_form(self):
        """
        Test redirect on blank load_form.

        :return:
        """
        response = self.client.get(reverse('load_tapwater_locations'))
        self.assertEqual(response.status_code, 302)

    def test_load_form_street_district(self):
        """
        Test ajax request for Districts with param city.

        :return:
        """
        response = self.client.get(reverse("load_tapwater_locations"),
                                   {"city": "Heilbronn"},
                                   **self.xml_http_request)
        self.assertEqual(response.status_code, 200)

    def test_load_form_street_zones(self):
        """
        Test ajax request for street zones with param city and district.

        :return:
        """
        response = self.client.get(reverse("load_tapwater_locations"),
                                   {"city": "Heilbronn",
                                    "district": "Sontheim"},
                                   **self.xml_http_request)
        self.assertEqual(response.status_code, 200)

    def test_show_tapwater_values(self):
        """
        Test request which is the selected showing tapwater values.

        Use param city, district and streetzone.

        :return:
        """
        response = self.client.get(reverse("show_tapwater_values"),
                                   {"city": "Heilbronn",
                                    "district": "Sontheim",
                                    "streetZone": "HN|Max-Planck-Str"
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="shareLinkButton"' in str(response.content))

        response = self.client.get(reverse("show_tapwater_values"),
                                   {"city": "Heilbronn",
                                    "district": "",
                                    "streetZone": "Test"
                                    })
        self.assertEqual(response.status_code, 200)

    def test_show_tapwater_no_values(self):
        """
        Test request which is the selected showing tapwater values.

        Use a wrong city as param

        :return:
        """
        response = self.client.get(reverse("show_tapwater_values"),
                                   {"city": "XYZ"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="shareLinkButton"' not in str(response.content))

    def test_show_tapwater_redirect(self):
        """Test the redirect to mainpage if no values given."""
        response = self.client.get(reverse("show_tapwater_values"))
        self.assertEqual(response.status_code, 302)

    def test_autocomplete_tapwater_redirect(self):
        """Test the autocomplete function."""
        response = self.client.get(reverse("autocomplete_tapwater_cities"))
        self.assertEqual(response.status_code, 302)

    def test_autocomplete_tapwater(self):
        """Test the autocomplete function."""
        response = self.client.get(reverse("autocomplete_tapwater_cities"),
                                   {
                                       "term": "Heilbronn"
                                   })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("autocomplete_tapwater_cities"),
                                   {
                                       "term": "Hei"
                                   })
        self.assertEqual(response.status_code, 200)
