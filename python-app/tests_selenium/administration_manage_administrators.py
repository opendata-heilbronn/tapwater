"""
Selenium test for import Add mineral water: #91.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""
import unittest
import time

from selenium import webdriver
from tests_selenium.settings import admin_url
from tests_selenium.utilities import login_admin, set_form_novalidate


class AddAdministrator(unittest.TestCase):
    """Selenium test for add mineral water."""

    username = "id_username"
    last_name = "id_last_name"
    first_name = "id_first_name"
    email = "id_email"

    new_password = "new_password"
    new_password_repeat = "new_password_repeat"

    user_to_delete = "UserOne"

    def setUp(self):
        """
        Setup selenium test.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_add_administrator(self):
        """
        Define the tests.

        :return:
        """
        login_admin(self.driver)
        add_admin_tests = [
            {
                self.username: self.user_to_delete,
                self.first_name: "user",
                self.last_name: "one",
                self.email: "user.one@localhost.de",
                "successful": True
            },
            {
                self.username: "",
                self.first_name: "user",
                self.last_name: "one",
                self.email: "user.eins@localhost.de",
                "successful": False
            },
            {
                self.username: self.user_to_delete,
                self.first_name: "",
                self.last_name: "one",
                self.email: "user.eins@localhost.de",
                "successful": False
            },
            {
                self.username: self.user_to_delete,
                self.first_name: "user",
                self.last_name: "",
                self.email: "user.eins@localhost.de",
                "successful": False
            },
            {
                self.username: self.user_to_delete,
                self.first_name: "user",
                self.last_name: "one",
                self.email: "user.eins",
                "successful": False
            },
            {
                self.username: "",
                self.first_name: "",
                self.last_name: "",
                self.email: "",
                "successful": False
            }
        ]

        for test in add_admin_tests:
            self.handle_add_test(test)

    def test_delete_administrator(self):
        """
        Test to delete a created administrator.

        :return:
        """
        login_admin(self.driver)
        driver = self.driver
        driver.get(admin_url + "administrators")
        driver.find_element_by_id("delete" + self.user_to_delete).click()
        time.sleep(1)
        driver.find_element_by_id("delete-successful")

    def test_change_password(self):
        """
        Define the tests.

        :return:
        """
        login_admin(self.driver)
        change_password_test = [
            {
                self.new_password: "newPassword",
                self.new_password_repeat: "newPassword",
                "successful": True
            },
            {
                self.new_password: "",
                self.new_password_repeat: "newPassword",
                "successful": False
            },
            {
                self.new_password: "newPassword",
                self.new_password_repeat: "",
                "successful": False
            },
            {
                self.new_password: "",
                self.new_password_repeat: "",
                "successful": False
            },
            {
                self.new_password: "newPassword",
                self.new_password_repeat: "newPasswordX",
                "successful": False
            },
            {
                self.new_password: "AdminWasser",  # set default password
                self.new_password_repeat: "AdminWasser",
                "successful": True
            }
        ]

        for test in change_password_test:
            self.handle_change_password_test(test)

    def handle_add_test(self, test):
        """
        Excecute test for adding administrators.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(admin_url + "administrators")

        set_form_novalidate(driver, "frmAddAdmin")

        username = driver.find_element_by_id(self.username)
        username.send_keys(test[self.username])

        first_name = driver.find_element_by_id(self.first_name)
        first_name.send_keys(test[self.first_name])

        last_name = driver.find_element_by_id(self.last_name)
        last_name.send_keys(test[self.last_name])

        email = driver.find_element_by_id(self.email)
        email.send_keys(test[self.email])

        driver.find_element_by_id("btnAddAdmin").click()

        time.sleep(2)

        if test["successful"]:
            driver.find_element_by_id("save-successful")

        if not test["successful"]:
            driver.find_element_by_id("save-failure")

    def handle_change_password_test(self, test):
        """
        Handle change password test.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(admin_url + "change/password/")

        set_form_novalidate(driver, "frmChangePassword")

        new_password = driver.find_element_by_id(self.new_password)
        new_password.send_keys(test[self.new_password])

        new_password_repeat = driver.find_element_by_id(
            self.new_password_repeat)
        new_password_repeat.send_keys(test[self.new_password_repeat])

        driver.find_element_by_id("btnChangePassword").click()

        time.sleep(2)

        if test["successful"]:
            driver.find_element_by_id("change-successful")

        if not test["successful"]:
            driver.find_element_by_id("change-failed")

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
