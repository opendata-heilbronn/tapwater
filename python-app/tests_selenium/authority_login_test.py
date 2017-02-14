"""
Selenium test for authority and private user login.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
from selenium import webdriver

from tests_selenium.settings import base_url


class AuthorityLogin(unittest.TestCase):
    """Test Class for authority user and private user login."""

    mail = "mail"

    def setUp(self):
        """
        Set up selenium test.

        :return:
        """
        self.base_url = base_url
        self.driver = webdriver.Firefox()

    def test_login_authority(self):
        """
         Create the test measurements as list.

        :return:
        """
        login_authority_tests = [
            {
                self.mail: "selenium@localhost",
                "successful": bool(True)
            },
            {
                self.mail: "jh",
                "successful": bool(False)
            },
            {
                self.mail: "unbekannt@unbekannt",
                "successful": bool(False)
            },
        ]

        for test in login_authority_tests:
            self.handle_test(test)

    def handle_test(self, test):
        """
        Excecute the test.

        :return:
        """
        driver = self.driver
        driver.get(base_url)
        element = driver.find_element_by_id(
            "login")
        element.click()
        time.sleep(1)
        driver.find_element_by_css_selector("input#id_email."
                                            "form-control").\
            send_keys(test[self.mail])

        driver.find_element_by_id("submit_login").click()
        time.sleep(1)

        if bool(test["successful"]) and \
                type(test["successful"] == bool):
            self.driver.find_element_by_css_selector("#successMessage")

        if not bool(test["successful"]) and \
                type(test["successful"] == bool):
            self.driver.find_element_by_css_selector("#failedMessage")

    def tearDown(self):
        """
        Close the driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
