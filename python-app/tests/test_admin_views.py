"""
test for admin views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""


import os

from django.test import TestCase
from django.urls import reverse

from tests.common import no_request_warning


class AdminViewsTest(TestCase):
    """Unit test class for admin views."""

    fixtures = ['tests/fixtures/tapwater_fixture.json',
                'tests/fixtures/users_fixture.json',
                'tests/fixtures/administration_fixture.json']
    admin_username = 'admin'
    admin_password = 'AdminWasser'

    def setUp(self):
        """
        Set up the unit test.

        :return:
        """
        self.client.login(username=self.admin_username,
                          password=self.admin_password)
        self.test_dir = os.getcwd() + "/tests_selenium/testdata/"

    def test_show_measurements(self):
        """
        Test view for measurements.

        :return:
        """
        response = self.client.get(reverse('show_measurements'))

        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_measurements'), {
            'page': "34l"
        })

        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_measurements'), {
            'page': None
        })

        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_measurements'), {
            'page': "-1"
        })

        self.assertEqual(response.status_code, 200)

    def test_show_mineral_waters(self):
        """
        Test view for mineral waters.

        :return:
        """
        response = self.client.get(reverse('show_mineral_waters'))
        self.assertEqual(response.status_code, 200)

    def test_show_average_measurement_value(self):
        """
        Test view for average measurement values.

        :return:
        """
        response = self.client.get(reverse('show_average_measurement_value'))
        self.assertEqual(response.status_code, 200)

    def test_show_nutrient_daily_dosis(self):
        """
        Test view for nutrient daily dosis.

        :return:
        """
        response = self.client.get(reverse('show_nutrient_daily_dosis'))
        self.assertEqual(response.status_code, 200)

    def test_import_measurements(self):
        """
        Test view for import measurements.

        :return:
        """
        response = self.client.get(reverse('import_measurements'))
        self.assertEqual(response.status_code, 200)

    def test_import_contacts(self):
        """
        Test view for import contacts.

        :return:
        """
        response = self.client.get(reverse('import_contacts'))
        self.assertEqual(response.status_code, 200)

    def test_show_users(self):
        """
        Test view for user values.

        :return:
        """
        response = self.client.get(reverse('show_users'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_users'), {
            'page': "34l"
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_users'), {
            'page': None
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_users'), {
            'page': "-1"
        })
        self.assertEqual(response.status_code, 200)

    def test_validate_form_import_measurements(self):
        """
        Check the import measurement form.

        :return:
        """
        data_locations = open(self.test_dir + 'mannheim_locations.json',
                              encoding='utf-8')
        data_zones = open(self.test_dir + 'mannheim_zones.json',
                          encoding='utf-8')
        region = "Best"
        self.client.request()
        with data_zones as dz, data_locations as dl:
            response = self.client.post(reverse("import_measurements"), {
                'zones': dz,
                'locations': dl,
                'region': region})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-successful"' in str(response.content))

        self.client.request()
        data_locations = open(self.test_dir + 'mannheim_locations.json',
                              encoding='utf-8')
        data_zones = open(self.test_dir + 'mannheim_zones.json',
                          encoding='utf-8')
        with data_zones as dzs, data_locations as dl:
            response = self.client.post(reverse("import_measurements"), {
                'zones': dzs,
                'locations': dl,
                'region': dl})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="failed-files"' in str(response.content))

        data_locations.close()
        data_zones.close()

        self.client.request()
        data_locations_f = open(self.test_dir +
                                'locations_hn_force_rollback.json',
                                encoding='utf-8')
        data_zones_f = open(self.test_dir + 'zones_hn_force_rollback.json',
                            encoding='utf-8')
        with data_zones_f as dzf, data_locations_f as dlf:
            response = self.client.post(reverse("import_measurements"), {
                'zones': dzf,
                'locations': dlf,
                'region': region})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="failed-files"' in str(response.content))

        data_locations_f.close()
        data_zones_f.close()

        self.client.request()
        data_locations = open(self.test_dir + 'locations_hn.json',
                              encoding='utf-8')
        data_zones_false = open(self.test_dir + 'man_zones_without_zone.json',
                                encoding='utf-8')
        with data_zones_false as dzff, data_locations as dl:
            response = self.client.post(reverse("import_measurements"), {
                'zones': dzff,
                'locations': dl,
                'region': region})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="failed-files"' in str(response.content))

        data_locations.close()
        data_zones_false.close()

    def test_validate_form_import_contacts(self):
        """
        Check the import contacts form.

        :return:
        """
        data_contacts = open(self.test_dir + 'contacts.csv', encoding='utf-8')
        self.client.request()
        with data_contacts as dc:
            response = self.client.post(reverse("import_contacts"), {
                'contacts': dc})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-successful"' in str(response.content))
        data_contacts.close()

        data_contacts_f = open(self.test_dir + 'contacts_missing_aet.csv',
                               encoding='utf-8')
        self.client.request()
        with data_contacts_f as dc:
            response = self.client.post(reverse("import_contacts"), {
                'contacts': dc})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="failed-files"' in str(response.content))
        data_contacts_f.close()

        self.client.request()
        response = self.client.post(reverse("import_contacts"), {
            'contacts': 's'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="failed-files"' in str(response.content))

        data_contacts_f = open(self.test_dir + 'contacts_force_rollback.csv',
                               encoding='utf-8')
        self.client.request()
        with data_contacts_f as dc:
            response = self.client.post(reverse("import_contacts"), {
                'contacts': dc})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="failed-files"' in str(response.content))
        data_contacts_f.close()

    def test_administration_index_page(self):
        """Test administration index page."""
        response = self.client.get(reverse("admin_index"))
        self.assertEqual(response.status_code, 200)

    def test_send_token_for_all_users(self):
        """
        Test create token for all users.

        :return:
        """
        response = self.client.get(reverse('send_token_for_all_users'))
        self.assertEqual(response.status_code, 200)

    def test_edit_average_measurement_value(self):
        """
        Test view for edit_average_measurement_value.

        :return:
        """
        # test show page
        response = self.client.get(reverse('edit_average_measurement_value'))
        self.assertEqual(response.status_code, 200)

        # test save successful
        form_data = {
            'sodium': 1.3,
            'potassium': 1.7,
            'calcium': 2.7,
            'magnesium': 2.7,
            'chloride': 1.7,
            'nitrate': 2.7,
            'sulfate': 2.7,
            'hardness': 2.4,
        }
        response = self.client.post(reverse('edit_average_measurement_value'),
                                    form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-successful"' in str(response.content))

        # test save failure
        form_data["sodium"] = ""
        response = self.client.post(reverse('edit_average_measurement_value'),
                                    form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-error"' in str(response.content))

    def test_show_select_users(self):
        """
        Test view for showing users to select.

        :return:
        """
        response = self.client.get(reverse('send_token_for_selected_users'))
        self.assertEqual(response.status_code, 200)

    def test_send_token_for_selected_users_successful(self):
        """
        Test sendmail successful.

        :return:
        """
        response = self.client.post(
            reverse("send_token_for_selected_users"), {
                'sendToken[]': [1]
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="send-successful"' in str(response.content))

        response = self.client.post(
            reverse("send_token_for_selected_users"), {
                'sendToken[]': []
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="send-warning"' in str(response.content))

    def test_send_token_for_selected_users_failure(self):
        """
        Test send mail failed.

        :return:
        """
        response = self.client.post(
            reverse("send_token_for_selected_users"), {
                'sendToken[]': [2]
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="send-failure"' in str(response.content))

    def test_send_token_for_selected_users_object_not_found(self):
        """
        Test send mail object not found.

        :return:
        """
        response = self.client.post(
            reverse("send_token_for_selected_users"), {
                'sendToken[]': [999]
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="send-failure"' in str(response.content))

    def test_show_locations(self):
        """
        Test view for locations.

        :return:
        """
        response = self.client.get(reverse('show_locations'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_locations'), {
            'page': "34l"
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_locations'), {
            'page': ""
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('show_locations'), {
            'page': "-1"
        })
        self.assertEqual(response.status_code, 200)

    def test_edit_mineral_water(self):
        """
        Test view for edit mineral water.

        :return:
        """
        # test show page
        response = self.client.get(reverse('edit_mineral_water',
                                           kwargs={"mineral_water_id": 2}))
        self.assertEqual(response.status_code, 200)

        # test save successful
        form_data = {
            'name': "Teusser",
            'key': "teusser",
            'sources': "www.google.de",
            'sodium': 1.3,
            'potassium': 1.7,
            'calcium': 2.7,
            'magnesium': 2.7,
            'chloride': 1.7,
            'nitrate': 2.7,
            'sulfate': 2.7
        }
        response = self.client.post(reverse('edit_mineral_water',
                                            kwargs={"mineral_water_id": 2}),
                                    form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-successful"' in str(response.content))

        # test save failure
        form_data["name"] = ""
        response = self.client.post(reverse('edit_mineral_water',
                                            kwargs={"mineral_water_id": 2}),
                                    form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failure"' in str(response.content))

        # test object not found
        with no_request_warning():
            response = self.client.get(reverse('edit_mineral_water',
                                               kwargs={
                                                   "mineral_water_id": 999}))
            self.assertEqual(response.status_code, 404)

    def test_add_mineral_water(self):
        """
        Test view for add mineral water.

        :return:
        """
        # test show page
        response = self.client.get(reverse('add_mineral_water'))
        self.assertEqual(response.status_code, 200)

        # test save successful
        form_data = {
            'name': "AquaQuelle",
            'key': "aqua",
            'sources': "www.google.de",
            'sodium': 1.3,
            'potassium': 1.7,
            'calcium': 2.7,
            'magnesium': 2.7,
            'chloride': 1.8,
            'nitrate': 2.7,
            'sulfate': 2.7
        }
        response = self.client.post(reverse('add_mineral_water'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-successful"' in str(response.content))

        # test save failure: name of mineral water is missing
        form_data["name"] = ""
        response = self.client.post(reverse('add_mineral_water'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failure"' in str(response.content))

        # test save failure: name already exists
        form_data["name"] = "Volvic"
        response = self.client.post(reverse('add_mineral_water'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failure"' in str(response.content))

        # test save failure: key already exists
        form_data["key"] = "teusser"
        response = self.client.post(reverse('add_mineral_water'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failure"' in str(response.content))

    def test_remove_mineral_water(self):
        """
        Test delete mineral water.

        :return:
        """
        response = self.client.get(reverse('delete_mineral_water',
                                           kwargs={"mineral_water_id": 3}))
        self.assertEqual(response.status_code, 302)
        with no_request_warning():
            response = self.client.get(reverse('delete_mineral_water',
                                               kwargs={
                                                   "mineral_water_id": 999
                                               }))
            self.assertEqual(response.status_code, 404)

    def test_confirm_authority_user(self):
        """
        Test view for showing users to select.

        :return:
        """
        response = self.client.get(reverse('confirm_authority_user'))
        self.assertEqual(response.status_code, 200)

    def test_confirm_authority_user_successful(self):
        """
        Test confirm authority successful.

        :return:
        """
        response = self.client.post(
            reverse("confirm_authority_user"), {
                'verifyUsers[]': [1]
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="send-successful"' in str(response.content))

        response = self.client.post(
            reverse("confirm_authority_user"), {
                'verifyUsers[]': []
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="send-warning"' in str(response.content))

    def test_confirm_authority_user_object_not_found(self):
        """
        Test send confirm authority object not found.

        :return:
        """
        response = self.client.post(
            reverse("confirm_authority_user"), {
                'verifyUsers[]': [999]
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="send-failure"' in str(response.content))

    def test_delete_user(self):
        """
        Test delete user.

        :return:
        """
        response = self.client.get(reverse('delete_user',
                                           kwargs={"user_id": 3}))
        self.assertEqual(response.status_code, 302)

    def test_show_history(self):
        """
        Test view for measurements history.

        :return:
        """
        response = self.client.get(reverse('show_history',
                                           kwargs={"location_id": 1}))

        self.assertEqual(response.status_code, 200)

    def test_manage_users(self):
        """
        Test manage users view.

        :return:
        """
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)

    def test_logout_admin(self):
        """
        Test for admin logout.

        :return:
        """
        response = self.client.get(reverse('admin_logout'))

        self.assertEqual(response.status_code, 302)

    def test_manage_administrators(self):
        """
        Test manage administration view.

        :return:
        """
        response = self.client.get(reverse('manage_administrators'))
        self.assertEqual(response.status_code, 200)

    def test_add_administrator(self):
        """
        Test add administrator.

        :return:
        """
        response = self.client.get(reverse('add_admin'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'username': "test_user",
            'first_name': "test",
            'last_name': "user",
            'email': "test.user@localhost.de"
        }

        # test save successful
        response = self.client.post(reverse('add_admin'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-successful"' in str(response.content))

        # test save failure - user exists
        form_data["username"] = "admin"
        response = self.client.post(reverse('add_admin'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failure"' in str(response.content))

        # test save failure - form invalid
        form_data["username"] = ""
        response = self.client.post(reverse('add_admin'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failure"' in str(response.content))

    def test_delete_administrator(self):
        """
        Test delete administrator.

        :return:
        """
        response = self.client.get(reverse('delete_admin',
                                           kwargs={"user_id": 1}))
        self.assertEqual(response.status_code, 302)
        with no_request_warning():
            response = self.client.get(reverse('delete_admin',
                                               kwargs={"user_id": 9999}))
            self.assertEqual(response.status_code, 200)

    def test_change_admin_password(self):
        """
        Test changing admin password.

        :return:
        """
        # test site request
        response = self.client.get(reverse('change_admin_password'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'new_password': "test",
            'new_password_repeat': ""
        }

        # test save failure emtpy value
        response = self.client.post(reverse('change_admin_password'),
                                    form_data)
        self.assertEqual(response.status_code, 302)

        # test save failure wrong values
        form_data["new_password_repeat"] = "testa"
        response = self.client.post(reverse('change_admin_password'),
                                    form_data)
        self.assertEqual(response.status_code, 302)

        # test save successful
        form_data["new_password_repeat"] = "test"
        response = self.client.post(reverse('change_admin_password'),
                                    form_data)
        self.assertEqual(response.status_code, 302)
