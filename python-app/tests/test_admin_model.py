"""
test for admin models.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""


from django.test import TestCase

import os
import json
import csv


from wasser.administration.models import (ImportMeasurementsDocument,
                                          ImportContactsDocument)


class AdminFormTest(TestCase):
    """Unit test class for admin models."""

    fixtures = ['tests/fixtures/administration_fixture.json']

    def setUp(self):
        """
        Set up the unit test.

        :return:
        """
        self.test_dir = os.getcwd() + "/tests_selenium/testdata/"

    def test_load_location_json(self):
        """
        Check the load_location_json function.

        :return:
        """
        data_locations = open(self.test_dir + 'mannheim_locations.json',
                              encoding='utf-8')
        locations_file = ImportMeasurementsDocument(locations=data_locations)
        data_locations_a = json.load(data_locations)
        data_locations.close()

        a = ImportMeasurementsDocument.load_location_json(locations_file)
        self.assertEqual(a, data_locations_a)

        data_locations_false = open(self.test_dir +
                                    'loc_without_loc_element.json',
                                    encoding='utf-8')
        locations_file_false = ImportMeasurementsDocument(
            locations=data_locations_false)
        data_locations_false.close()

        b = ImportMeasurementsDocument.load_location_json(locations_file_false)
        self.assertEqual(b, False)

        data_locations_false = open(self.test_dir +
                                    'mannheim_locations_cod.json',
                                    encoding='cp1252')
        locations_file_false = ImportMeasurementsDocument(
            locations=data_locations_false)
        data_locations_false.close()

        c = ImportMeasurementsDocument.load_location_json(locations_file_false)
        self.assertEqual(c, False)

    def test_load_zone_json(self):
        """
        Check the load_zone_json function.

        :return:
        """
        data_zones = open(self.test_dir + 'mannheim_zones.json',
                          encoding='utf-8')
        zones_file = ImportMeasurementsDocument(zones=data_zones)
        data_zones_a = json.load(data_zones)
        data_zones.close()

        a = ImportMeasurementsDocument.load_zone_json(zones_file)
        self.assertEqual(a, data_zones_a)

        data_zones_false = open(self.test_dir + 'contacts.csv',
                                encoding='utf-8')
        zones_file_false = ImportMeasurementsDocument(
            zones=data_zones_false)
        data_zones_false.close()

        b = ImportMeasurementsDocument.load_zone_json(zones_file_false)
        self.assertEqual(b, False)

    def test_is_valid_json_location(self):
        """
        Check the is_valid_json_location function.

        :return:
        """
        data_locations = open(self.test_dir + 'mannheim_locations.json',
                              encoding='utf-8')
        locations_file = ImportMeasurementsDocument(locations=data_locations)
        data_locations.close()

        a = ImportMeasurementsDocument.is_valid_json_location(locations_file)
        self.assertEqual(a, True)

        data_locations_false = open(self.test_dir +
                                    'loc_without_loc_element.json',
                                    encoding='utf-8')
        locations_file_false = ImportMeasurementsDocument(
            locations=data_locations_false)
        data_locations_false.close()

        b = ImportMeasurementsDocument.is_valid_json_location(
            locations_file_false)
        self.assertEqual(b, False)

        data_locations_false = open(self.test_dir +
                                    'mannheim_locations_cod.json',
                                    encoding='cp1252')
        locations_file_false = ImportMeasurementsDocument(
            locations=data_locations_false)
        data_locations_false.close()

        c = ImportMeasurementsDocument.is_valid_json_location(
            locations_file_false)
        self.assertEqual(c, False)

    def test_is_valid_json_zone(self):
        """
        Check the is_valid_json_zone function.

        :return:
        """
        data_zones = open(self.test_dir + 'mannheim_zones.json',
                          encoding='utf-8')
        zones_file = ImportMeasurementsDocument(zones=data_zones)
        data_zones.close()

        a = ImportMeasurementsDocument.is_valid_json_zone(zones_file)
        self.assertEqual(a, True)

        data_zones_false = open(self.test_dir + 'contacts.csv',
                                encoding='utf-8')
        zones_file_false = ImportMeasurementsDocument(
            zones=data_zones_false)
        data_zones_false.close()

        b = ImportMeasurementsDocument.load_zone_json(zones_file_false)
        self.assertEqual(b, False)

        data_zone_false = open(self.test_dir + 'mannheim_zones_cod.json',
                               encoding='cp1252')
        zones_file_false = ImportMeasurementsDocument(
            zones=data_zone_false)
        data_zone_false.close()

        c = ImportMeasurementsDocument.is_valid_json_zone(
            zones_file_false)
        self.assertEqual(c, False)

    def test_load_contacts_csv(self):
        """
        Check the load_contacts_csv function.

        :return:
        """
        data_contacts = open(self.test_dir + 'contacts.csv',
                             encoding='utf-8')
        contacts_file = ImportContactsDocument(contacts=data_contacts)

        with open(self.test_dir + 'contacts.csv', encoding='utf-8') as f:
            data_contacts_a = csv.reader(f, dialect=csv.excel,
                                         delimiter=';', skipinitialspace=True)
            next(data_contacts_a, None)
            csv_data_list_a = list(data_contacts_a)

        data_contacts.close()

        a = ImportContactsDocument.load_contacts_csv(contacts_file)
        self.assertEqual(a, csv_data_list_a)

        data_contacts_false_b = open(self.test_dir + 'contacts_code.csv',
                                     encoding='cp1252')
        contacts_file_false_b = ImportContactsDocument(
            contacts=data_contacts_false_b)
        data_contacts_false_b.close()

        b = ImportContactsDocument.load_contacts_csv(contacts_file_false_b)
        self.assertEqual(b, False)

    def test_is_valid_csv(self):
        """
        Check the is_valid_csv function.

        :return:
        """
        data_contacts = open(self.test_dir + 'contacts.csv', encoding='utf-8')
        contacts_file = ImportContactsDocument(contacts=data_contacts)
        data_contacts.close()

        a = ImportContactsDocument.is_valid_csv(contacts_file)
        self.assertEqual(a, True)

        data_contacts_false = open(self.test_dir +
                                   'contacts_wrong_column.csv',
                                   encoding='utf-8')
        contacts_file_false = ImportContactsDocument(
            contacts=data_contacts_false)
        data_contacts_false.close()

        b = ImportContactsDocument.is_valid_csv(contacts_file_false)
        self.assertEqual(b, False)

        data_contacts_false_c = open(self.test_dir +
                                     'contacts_missing_aet.csv',
                                     encoding='utf-8')
        contacts_file_false_c = ImportContactsDocument(
            contacts=data_contacts_false_c)
        data_contacts_false_c.close()

        c = ImportContactsDocument.is_valid_csv(contacts_file_false_c)
        self.assertEqual(c, False)

        data_contacts_false_d = open(self.test_dir +
                                     'contacts_4_columns.csv',
                                     encoding='utf-8')
        contacts_file_false_d = ImportContactsDocument(
            contacts=data_contacts_false_d)
        data_contacts_false_d.close()

        d = ImportContactsDocument.is_valid_csv(contacts_file_false_d)
        self.assertEqual(d, False)

        data_contacts_false_e = open(self.test_dir + 'contacts_code.csv',
                                     encoding='cp1252')
        contacts_file_false_e = ImportContactsDocument(
            contacts=data_contacts_false_e)
        data_contacts_false_e.close()

        e = ImportContactsDocument.is_valid_csv(contacts_file_false_e)
        self.assertEqual(e, False)
