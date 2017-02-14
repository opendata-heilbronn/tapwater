"""
test for login views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schaefer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""
from django.test import TestCase
from django.urls import reverse

from tests.common import no_request_warning


class LoginViewsTest(TestCase):
    """Unit test class for login views."""

    fixtures = ['tests/fixtures/administration_fixture.json']
    value = "d1d26d4aa203450d9492bf84fa9c3762"
    token = "111111aaaallslslslsls"
    user_id = 1
    no_id = ""
    admin_username = 'admin'
    admin_password = 'AdminWasser'

    def test_show_login_authority(self):
        """
        Test page of office login.

        :return:

        """
        response = self.client.get(reverse("login_authority"), {
            'token': self.value,
            'id': self.user_id,
        })
        self.assertEqual(response.status_code, 302)

    def test_show_login_authority_false_user(self):
        """
        Test page of office login.

        :return:

        """
        response = self.client.get(reverse("login_authority"), {
            'token': self.value,
            'id': self.no_id,
        })
        self.assertEqual(response.status_code, 302)

    def test_show_login_office_false_token(self):
        """
        Test page of office login.

        :return:

        """
        with no_request_warning():
            response = self.client.get(reverse("login_authority"), {
                'token': self.token,
                'id': self.user_id,
            })
            self.assertEqual(response.status_code, 404)

    def test_login_admin(self):
        """
        Test page of admin login.

        :return:

        """
        # test showing page
        response = self.client.get(reverse("admin_login"))
        self.assertEqual(response.status_code, 200)

        # test login successful
        response = self.client.post(reverse("admin_login"), {
            "user": self.admin_username,
            "password": self.admin_password
        })
        self.assertEqual(response.status_code, 302)

        # test login failed
        response = self.client.post(reverse("admin_login"), {
            "user": "",
            "password": ""
        })
        self.assertEqual(response.status_code, 200)

        # test login failed
        response = self.client.post(reverse("admin_login"), {
            "user": self.admin_username,
            "password": "xxx"
        })
        self.assertEqual(response.status_code, 200)

    def test_login_failed(self):
        """
        Test login failed page.

        :return:
        """
        response = self.client.get(reverse("admin_login_failed"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("user_login_failed"))
        self.assertEqual(response.status_code, 200)
