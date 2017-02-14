"""
Selenium test for import measurements.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
from selenium import webdriver
from tests_selenium.settings import test_dir, admin_url
from tests_selenium.utilities import login_admin


class ImportContacts(unittest.TestCase):
    """Selenium test for measurement imports."""

    contacts = "contacts"

    def setUp(self):
        """
        Set up driver.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_import_measurement(self):
        """
        Define the tests.

        :return:
        """
        import_contacts_tests = [
            {
                self.contacts: test_dir + "contacts.csv",
                "successful": True
            },
            {
                self.contacts: test_dir + "contacts_force_rollback.csv",
                "successful": False
            },
            {
                self.contacts: test_dir + "contacts_wrong_structure.csv",
                "successful": False
            },
        ]

        login_admin(self.driver)

        for test in import_contacts_tests:
            self.handle_test(test)

    def handle_test(self, test):
        """
        Execute test.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(admin_url + "authority/import/")
        driver.find_element_by_id("id_contacts").send_keys(test[self.contacts])

        # find the send button
        driver.find_element_by_id("submit").click()
        time.sleep(10)

        if test["successful"]:
            # find the successful box
            driver.find_element_by_id("save-successful")

        if not test["successful"]:
            # find the failed box
            driver.find_element_by_id("failed-files")

        # driver.refresh()

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
