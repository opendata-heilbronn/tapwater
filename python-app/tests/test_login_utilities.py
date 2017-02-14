"""
test for login utilities.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.test import TestCase
from django.urls import reverse

from wasser.login.utilities import (token_valid)
from wasser.administration.models import Token


class LoginUtilitiesTest(TestCase):
    """Class for Login utilities."""

    fixtures = ['tests/fixtures/administration_fixture.json']
    user_id = 1
    user_id_invalid_token = 3
    token = "d1d26d4aa203450d9492bf84fa9c3762"
    invalid_token = "a2e6d4aa203450d9492bf84fa9c3984"
    admin_username = 'admin'
    admin_password = 'AdminWasser'

    def test_token_valid(self):
        """
        Test if token is valid.

        :return:
        """
        current_token = Token.objects.get(user_id=self.user_id,
                                          value=self.token)

        a = token_valid(current_token)
        self.assertEqual(a, True)

    def test_token_not_valid(self):
        """
        Test if token is valid.

        :return:
        """
        current_token = Token.objects.get(user_id=self.user_id_invalid_token,
                                          value=self.invalid_token)

        a = token_valid(current_token)
        self.assertEqual(a, False)

    def test_admin_login_required(self):
        """
        Test if token is valid.

        :return:
        """
        self.response = self.client.get(reverse('admin_index'))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'login/admin_login_failed.html')

    def test_admin_login_success(self):
        """
        Test if login is succeed.

        :return:
        """
        self.client.login(username=self.admin_username,
                          password=self.admin_password)
        self.response = self.client.get(reverse('admin_index'))
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'administration/index.html')
