"""
test for users views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.test import TestCase
from django.urls import reverse


class UsersViewsTest(TestCase):
    """Unit test class for users views."""

    fixtures = ['tests/fixtures/administration_fixture.json',
                'tests/fixtures/users_fixture.json']
    value = "d1d26d4aa203450d9492bf84fa9c3762"
    user_id = 1

    def setUp(self):
        """Setup unit test."""
        self.test_post = {
            'city': 'Heilbronn',
            'region': 'Heilbronn',
            'district': 'Böckingen',
            'potassium': '1',
            'sodium': '2',
            'calcium': '3-4',
            'magnesium': '2',
            'chloride': '10',
            'nitrate': '1',
            'sulfate': '6',
            'degree_of_hardness': '35',
            'user': '1',
            'date': '12.12.2016',
            'source': 'Wikipedia',
            'remarks': 'No remark',
            'street1': 'Wollhausstraße',
            'zone1': 'Mitte'
        }
        self.test_user_post = {
            'firstname': 'Hans',
            'lastname': 'Peter',
            'email': 'email@menot.va'
        }

        # create session
        session = self.client.session
        session["user"] = self.user_id
        session["token"] = self.value
        session.save()

    def test_show_insert_measurement(self):
        """Test show insert measurement."""
        response = self.client.get(reverse("insert_measurement"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/insert_measurement.html')

    def test_post_insert_measurement_success(self):
        """Test post of insert measurement."""
        test_post = self.test_post
        response = self.client.post(reverse("insert_measurement"), test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-successful"' in str(response.content))
        self.assertTemplateUsed(response, 'users/insert_measurement.html')

        test_post = self.test_post
        response = self.client.post(reverse("insert_measurement"), test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-successful"' in str(response.content))
        self.assertTemplateUsed(response, 'users/insert_measurement.html')

    def test_post_insert_measurement_chloride_empty(self):
        """Test post of insert measurement."""
        test_post = self.test_post
        test_post["chloride"] = ""

        response = self.client.post(reverse("insert_measurement"), test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failed"' in str(response.content))
        self.assertTemplateUsed(response, 'users/insert_measurement.html')

    def test_post_insert_measurement_potassium_empty(self):
        """Test post of insert measurement."""
        test_post = self.test_post
        test_post["potassium"] = ""

        response = self.client.post(reverse("insert_measurement"), test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failed"' in str(response.content))
        self.assertTemplateUsed(response, 'users/insert_measurement.html')

    def test_post_insert_measurement_location_empty(self):
        """Test post of insert measurement."""
        test_post = self.test_post
        test_post["city"] = ""

        response = self.client.post(reverse("insert_measurement"), test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failed"' in str(response.content))
        self.assertTemplateUsed(response, 'users/insert_measurement.html')

    def test_post_insert_measurement_date_empty(self):
        """Test post of insert measurement."""
        test_post = self.test_post
        test_post["date"] = ""

        response = self.client.post(reverse("insert_measurement"), test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failed"' in str(response.content))
        self.assertTemplateUsed(response, 'users/insert_measurement.html')

    def test_post_insert_measurement_date_no_digit(self):
        """Test post of insert measurement."""
        test_post = self.test_post
        test_post["date"] = "abcd"

        response = self.client.post(reverse("insert_measurement"), test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="save-failed"' in str(response.content))
        self.assertTemplateUsed(response, 'users/insert_measurement.html')

    def test_index_page(self):
        """Test user index page."""
        response = self.client.post(reverse("users_index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')

    def test_show_measurements_user(self):
        """Test my measurements page."""
        response = self.client.post(reverse("show_measurements_user"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/show_measurements.html')

    def test_send_token_for_one_user_success(self):
        """Test token send to one user with invalid token."""
        response = self.client.get(reverse("send_token_for_one_user"))
        self.assertEqual(response.status_code, 200)

        test_post = self.test_user_post
        test_post["authority_mail"] = "hans.peter@localhost"

        response = self.client.post(reverse("send_token_for_one_user"),
                                    test_post)
        self.assertEqual(response.status_code, 200)

    def test_send_token_for_one_user_failed(self):
        """Test token send to one user with invalid token."""
        test_post = self.test_user_post
        test_post["authority_mail"] = ""
        response = self.client.post(reverse("send_token_for_one_user"),
                                    test_post)
        self.assertEqual(response.status_code, 200)

        test_post["authority_mail"] = "xyz@test.de"
        response = self.client.post(reverse("send_token_for_one_user"),
                                    test_post)
        self.assertEqual(response.status_code, 200)

    def test_registration_private_person(self):
        """Test private user registration page."""
        response = self.client.post(reverse("registration"))
        self.assertEqual(response.status_code, 302)

        self.client.logout()
        response = self.client.post(reverse("registration"))
        self.assertEqual(response.status_code, 200)

    def test_registration_private_person_empty_email(self):
        """Test user registration empty email."""
        self.client.logout()
        test_post = self.test_user_post
        test_post["email"] = ""

        response = self.client.post(reverse("registration"),
                                    test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="user-save-failed"' in str(response.content))

    def test_registration(self):
        """Test user registration page."""
        self.client.logout()
        response = self.client.post(reverse("registration"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("registration"))
        self.assertEqual(response.status_code, 200)

    def test_registration_private_person_success(self):
        """Test user registration success."""
        self.client.logout()
        test_post = self.test_user_post

        response = self.client.post(reverse("registration"),
                                    test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="user-save-successful"' in str(response.content))

    def test_registration_private_person_empty_username(self):
        """Test user registration empty username."""
        self.client.logout()
        test_post = self.test_user_post
        test_post["firstname"] = ""
        test_post["lastname"] = ""

        response = self.client.post(reverse("registration"),
                                    test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="user-save-failed"' in str(response.content))

    def test_registration_private_person_identical_mail(self):
        """Test user registration two identical email address."""
        self.client.logout()
        test_post = self.test_user_post

        response = self.client.post(reverse("registration"),
                                    test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="user-save-successful"' in str(response.content))

        response = self.client.post(reverse("registration"),
                                    test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="user-save-failed"' in str(response.content))

    def test_registration_authority(self):
        """Test user registration empty username."""
        self.client.logout()
        test_post = self.test_user_post
        test_post["email"] = "test@localhost.de"
        test_post["authority"] = True

        response = self.client.post(reverse("registration"),
                                    test_post)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id="user-save-successful"' in str(response.content))

    def test_users_logout(self):
        """
        Test users logut.

        :return:
        """
        response = self.client.get(reverse("users_logout"))
        self.assertEqual(response.status_code, 302)
