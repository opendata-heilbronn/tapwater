"""
Selenium test for user registration.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
import random
from selenium import webdriver
from tests_selenium.settings import users_url


class UserRegistration(unittest.TestCase):
    """Test Class for user registration."""

    firstname = "firstname"
    lastname = "lastname"
    email = "email"
    authority = "authority"

    def setUp(self):
        """
        Set up selenium test.

        :return:
        """
        self.driver = webdriver.Firefox()
        random.seed()

    def test_register_user(self):
        """
        Create the test measurements as list.

        :return:
        """
        user_registration_tests = [
            {
                self.firstname: "Max",
                self.lastname: "Meier",
                self.email: "max" + str(random.randint(1, 1000)) +
                            "@meies.dzt",
                self.authority: "Stadt Heilbronn",
                "successful": bool(True)
            },
            {
                self.firstname: "Heilbronn",
                self.lastname: "Heilbronn",
                self.email: "sasda",
                self.authority: "Stadt Heilbronn",
                "successful": bool(False)
            },
            {
                self.firstname: " ",
                self.lastname: " ",
                self.email: " ",
                self.authority: " ",
                "successful": bool(False)
            },

        ]

        for test in user_registration_tests:
            self.handle_test(test)

    def handle_test(self, test):
        """
        Excecute the test.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(users_url + "registration/private")
        firstname = driver.find_element_by_name(self.firstname)
        firstname.send_keys(test[self.firstname])
        lastname = driver.find_element_by_name(self.lastname)
        lastname.send_keys(test[self.lastname])
        email = driver.find_element_by_name(self.email)
        email.send_keys(test[self.email])
        self.driver.execute_script(
            "document.getElementById('id_authority_checkbox').value='True'")
        self.driver.find_element_by_id("id_authority_checkbox").click()
        authority = driver.find_element_by_name(self.authority)
        authority.send_keys(test[self.authority])

        # find the send button
        driver.find_element_by_id("submit").click()
        time.sleep(1)

        if bool(test["successful"]) and \
                type(test["successful"] == bool):
            self.driver.find_element_by_id("user-save-successful")

        if not bool(test["successful"]) and \
                type(test["successful"] == bool):
            self.driver.find_element_by_id("user-save-failed")

    def tearDown(self):
        """
        Close the driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
