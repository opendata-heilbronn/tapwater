"""
test for admin forms.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""


import os

from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from wasser.administration.forms import (validate_text_input,
                                         validate_file_extension_csv,
                                         validate_file_extension_json)


class AdminFormTest(TestCase):
    """Unit test class for admin utilities."""

    fixtures = ['tests/fixtures/administration_fixture.json']

    def setUp(self):
        """
        Set up the unit test.

        :return:
        """
        self.test_dir = os.getcwd() + "/tests_selenium/testdata/"

    def test_validate_form_import_measurements(self):
        """
        Check the import measurement form.

        :return:
        """
        data_locations = open(self.test_dir + 'mannheim_locations.json',
                              encoding='utf-8')
        data_zones = open(self.test_dir + 'mannheim_zones.json',
                          encoding='utf-8')
        region = "Bayern"
        with data_zones as fp, data_locations as f:
            response = self.client.post(reverse("insert_measurement"), {
                                                            'zones': fp,
                                                            'locations': f,
                                                            'region': region})

        data_locations.close()
        data_zones.close()
        self.assertEqual(response.status_code, 200)

    def test_validate_text_input(self):
        """
        Check region name field.

        :return:
        """
        region = "Bayern"
        region_false = "B"
        a = validate_text_input(region)
        self.assertEqual(a, None)
        with self.assertRaises(ValidationError) as context:
            validate_text_input(region_false)
        self.assertTrue("Kein gültiger Wert für Region" or
                        "No valid value for region" in
                        str(context.exception))

    def test_validate_form_import_contacts(self):
        """
        Check the import contacts form.

        :return:
        """
        data_contacts = open(self.test_dir + 'contacts.csv',
                             encoding='utf-8')
        with data_contacts as contacts:
            response = self.client.post(reverse("import_contacts"), {
                'contacts': contacts})
        data_contacts.close()
        self.assertEqual(response.status_code, 200)

    def test_validate_file_extension_csv(self):
        """
        Check if the csv file has a correct extension.

        :return:
        """
        data_contacts = open(self.test_dir + 'contacts.csv',
                             encoding='utf-8')
        data_contacts_false = open(self.test_dir + 'mannheim_short.json',
                                   encoding='utf-8')
        a = validate_file_extension_csv(data_contacts)
        self.assertEqual(a, None)
        with self.assertRaises(ValidationError) as context:
            validate_file_extension_csv(data_contacts_false)
        data_contacts.close()
        data_contacts_false.close()
        self.assertTrue("Keine gültige CSV-Datei" or "No valid CSV file" in
                        str(context.exception))

    def test_validate_file_extension_json(self):
        """
        Check if the json file has a correct extension.

        :return:
        """
        data_locations = open(self.test_dir + 'mannheim_short.json',
                              encoding='utf-8')
        data_locations_false = open(self.test_dir + 'contacts.csv',
                                    encoding='utf-8')
        a = validate_file_extension_json(data_locations)
        self.assertEqual(a, None)
        with self.assertRaises(ValidationError) as context:
            validate_file_extension_json(data_locations_false)
        data_locations.close()
        data_locations_false.close()
        self.assertTrue("Kein gültiges JSON-File" or "No valid JSON file" in
                        str(context.exception))
