"""
Selenium test for user types(#2).

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
from selenium import webdriver

from tests_selenium.settings import login_url


class LoginUsers(unittest.TestCase):
    """
    Test class for users.

    :return:
    """

    def setUp(self):
        """
        Set up selenium test.

        :return:
        """
        self.login_url = login_url
        self.driver = webdriver.Firefox()

    def test_users_private_login(self):
        """
        Login as private.

        :return:
        """
        driver = self.driver
        driver.get(login_url)
        driver.find_element_by_id("btn-login2").click()
        time.sleep(1)
        driver.get(login_url)
        driver.find_element_by_id("btn-login").click()
        time.sleep(1)

    def tearDown(self):
        """
        Close the driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
