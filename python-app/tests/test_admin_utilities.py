"""
test for admin utilities.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""


from django.test import TestCase
import json
import os

from wasser.administration.utilities import (insert_measurement_to_database,
                                             insert_user_to_database,
                                             user_not_exists,
                                             get_key,
                                             check_rollback,
                                             flattens)
from wasser.login.utilities import save_token
from wasser.administration.models import (ImportMeasurementsDocument)


class AdminUtilitiesTest(TestCase):
    """Unit test class for admin utilities."""

    fixtures = ['tests/fixtures/administration_fixture.json']
    user_id = 1
    token = "d1d26d4aa203450d9492bf84fa9c3762"

    def setUp(self):
        """
        Set up the unit test.

        :return:
        """
        self.test_dir = os.getcwd() + "/tests_selenium/testdata/"

    def test_insert_measurement_to_database(self):
        """
        Test the function for insert measurements to database.

        :return:
        """
        key = 'Obersulm Affaltrach'
        value = ''
        region = 'Bayern'
        with open(self.test_dir + '/zones_hn.json', encoding='utf-8') as file:
            data_zones = json.load(file)

            a = insert_measurement_to_database(key, value, data_zones, region)
            self.assertEqual(a, True)

            key = 'Kein Ort'
            b = insert_measurement_to_database(key, value, data_zones, region)
            self.assertEqual(b, False)

            key = 'Abstatt Kernstadt Zone 3'
            c = insert_measurement_to_database(key, value, data_zones, region)
            self.assertEqual(c, True)

            key = 'Wüstenrot'
            d = insert_measurement_to_database(key, value, data_zones, region)
            self.assertEqual(d, True)

    def test_insert_user_to_database(self):
        """
        Test the function for insert users to database.

        :return:
        """
        row = ['Hans', 'Peter', 'hans.peter@localhost', 'Stadt Heilbronn']
        contact_firstname = "Hans"
        contact_lastname = "Peter"
        contact_mail = "hans.peter@localhost"
        municipalitie = "Stadt Heilbronn"
        a = insert_user_to_database(row, contact_firstname,
                                    contact_lastname,
                                    contact_mail,
                                    municipalitie)
        self.assertEqual(a, True)

    def test_user_not_exists(self):
        """
        Test the function for checking if user does not already exists.

        :return:
        """
        row = ['Hans Peter', 'hans.peter@localhost', 'Stadt Heilbronn']
        contact_firstname = "Hans"
        contact_lastname = "Peter"
        contact_mail = "hans.peter@localhost"
        municipalitie = "Stadt Heilbronn"

        a = user_not_exists(row, contact_firstname,
                            contact_lastname,
                            contact_mail,
                            municipalitie)
        self.assertEqual(a, False)

        municipalitie = "Gemeinde Neue"
        b = user_not_exists(row, contact_firstname,
                            contact_lastname,
                            contact_mail,
                            municipalitie)
        self.assertEqual(b, True)

    def test_get_key(self):
        """
        Test the function that returns the key string for insert measurement.

        :return:
        """
        city = "Bad Friedrichshall"
        suburb = "Kochendorf"
        zone = "Nord"
        a = get_key(city, suburb, zone)
        self.assertEqual(a, "Bad Friedrichshall Kochendorf Nord")

        city = "Wüstenrot"
        suburb = ""
        zone = ""
        b = get_key(city, suburb, zone)
        self.assertEqual(b, "Wüstenrot")

        city = "Obersulm"
        suburb = "Affaltrach"
        zone = ""
        c = get_key(city, suburb, zone)
        self.assertEqual(c, "Obersulm Affaltrach")

        city = "Heilbronn"
        suburb = ""
        zone = "14"
        d = get_key(city, suburb, zone)
        self.assertEqual(d, "Heilbronn 14")

    def test_check_rollback(self):
        """
        Test if rollback for the measurement import is necessary.

        :return:
        """
        data_zones = open(self.test_dir + 'mannheim_zones.json',
                          encoding='utf-8')
        data_locations = open(self.test_dir + 'mannheim_locations.json',
                              encoding='utf-8')
        data_zones_false = open(self.test_dir + 'man_zones_force_rb.json',
                                encoding='utf-8')
        locations_file = ImportMeasurementsDocument(locations=data_locations)
        zones_file = ImportMeasurementsDocument(zones=data_zones)
        region = "Bayern"
        data_zones.close()
        data_locations.close()

        a = check_rollback(locations_file, zones_file, region)
        self.assertEqual(a, False)
        zones_file = ImportMeasurementsDocument(zones=data_zones_false)
        data_zones_false.close()
        b = check_rollback(locations_file, zones_file, region)
        data_zones_false.close()
        self.assertEqual(b, True)

    def test_flattens(self):
        """
        Test running through the location file structure.

        :return:
        """
        data_locations = open(self.test_dir + 'mannheim_locations.json',
                              encoding='utf-8')
        locations_file = ImportMeasurementsDocument(locations=data_locations)
        data_locations.close()
        a = flattens(locations_file.load_location_json())
        valid = False
        if 'Locations_Meckenheim, Pfalz' in a and len(a) == 111:
            valid = True
        self.assertEqual(valid, True)

    def test_save_token(self):
        """
        Test save token in Database.

        :return:
        """
        a = save_token(self.user_id, self.token)
        self.assertTrue(a)
