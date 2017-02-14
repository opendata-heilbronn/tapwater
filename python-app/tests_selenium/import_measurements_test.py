"""
Selenium test for import measurements.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
from selenium import webdriver
from tests_selenium.settings import test_dir, admin_url
from tests_selenium.utilities import login_admin


class ImportMeasurement(unittest.TestCase):
    """Selenium test for measurement imports."""

    locations = "locations"
    zones = "zones"
    region = "region"

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
        import_measurement_tests = [
            {
                self.region: "Heilbronn",
                self.locations: test_dir + "locations_hn.json",
                self.zones: test_dir + "zones_hn.json",
                "successful": True
            },
            {
                self.region: "Heilbronn",
                self.locations: test_dir + "wrong_type.html",
                self.zones: test_dir + "zones_hn.json",
                "successful": False
            },
            {
                self.region: "Heilbronn",
                self.locations: test_dir + "locations_hn.json",
                self.zones: test_dir + "wrong_type.html",
                "successful": False
            },
            {
                self.region: "Heilbronn",
                self.locations: test_dir + "wrong_structure.json",
                self.zones: test_dir + "zones_hn.json",
                "successful": False
            },
            {
                self.region: "Heilbronn",
                self.locations: test_dir + "locations_hn_force_rollback.json",
                self.zones: test_dir + "zones_hn_force_rollback.json",
                "successful": False
            },
            {
                self.region: "H",
                self.locations: test_dir + "locations_hn.json",
                self.zones: test_dir + "zones_hn.json",
                "successful": False
            },
        ]

        login_admin(self.driver)

        for test in import_measurement_tests:
            self.handle_test(test)

    def handle_test(self, test):
        """
        Execute test.

        :param test:
        :return:
        """
        driver = self.driver
        # driver.implicitly_wait(20)
        driver.get(admin_url + "measurement/import/")
        region = driver.find_element_by_id("id_region")
        region.send_keys(test[self.region])
        location = driver.find_element_by_id("id_locations")
        location.send_keys(test[self.locations])
        zone = driver.find_element_by_id("id_zones")
        zone.send_keys(test[self.zones])

        driver.implicitly_wait(5)

        # find the send button
        driver.find_element_by_id("submit").click()

        if test["successful"]:
            # find the successful box
            driver.find_element_by_id("save-successful")

        if not test["successful"]:
            # find the failed box
            driver.find_element_by_id("failed-files")

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
