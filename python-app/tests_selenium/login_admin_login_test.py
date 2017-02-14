"""
Selenium test for admin registration(#32).

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
from selenium import webdriver

from tests_selenium.settings import login_url


class LoginAdmin(unittest.TestCase):
    """Test Class for admin registration."""

    username = "user"
    password = "password"

    def setUp(self):
        """
        Set up selenium test.

        :return:
        """
        self.login_url = login_url + "admin"
        self.driver = webdriver.Firefox()

    def test_login_admin(self):
        """
        Login as a administrator.

        :return:
        """
        admin_registration_tests = [
            {
                self.username: "Heilbronn",
                self.password: "sasda",
                "successful": bool(False)
            },
            {
                self.username: " ",
                self.password: " ",
                "successful": bool(False)
            },
            {
                self.username: "admin",
                self.password: "AdminWasser",
                "successful": bool(True)
            },
        ]

        for test in admin_registration_tests:
            self.handle_test(test)

    def handle_test(self, test):
        """
        Excecute the test.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(login_url + "admin")
        driver.find_element_by_id("user").send_keys(test[self.username])
        driver.find_element_by_id("password").send_keys(test[self.password])
        driver.find_element_by_id("submit").click()

        time.sleep(1)

        if bool(test["successful"]) and type(test["successful"] == bool):
            self.driver.find_elements_by_id("admin-save-successful")

        if not bool(test["successful"]) and type(test["successful"] == bool):
            self.driver.find_elements_by_id("admin-login-failed")

    def tearDown(self):
        """
        Close the driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
