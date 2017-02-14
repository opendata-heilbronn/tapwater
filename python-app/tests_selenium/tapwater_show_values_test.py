"""
Selenium test for tapwater street zones.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schaefer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
from selenium import webdriver
from tests_selenium.settings import base_url


class TapwaterStreetZones(unittest.TestCase):
    """Selenium test for measurement imports."""

    city = "city"
    district = "district"
    street_zone = "streetZone"

    location_correct = "shareLinkButton"
    location_not_correct = "shareLinkButton"

    def setUp(self):
        """
        Set up driver.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_show_tapwater_values(self):
        """
        Check tapwater values.

        :return:
        """
        show_tapwater_values_tests = [
            {
                self.city: "Massenbachhausen",
                self.district: "",
                self.street_zone: "",
                "location_correct": True
            },
            {
                self.city: "Beilstein",
                self.district: "Beilstein",
                self.street_zone: "Hochbehälter+Langhans+"
                                  "(Beilstein+Ost)|Amselweg",
                "location_correct": True
            },
            {
                self.city: "Heilbronn",
                self.district: "",
                self.street_zone: "14-18%7CAchtungstraße",
                "location_correct": True
            },
            {
                self.city: "Xyz",
                self.district: "",
                self.street_zone: "",
                "location_correct": False
            }
        ]
        for test in show_tapwater_values_tests:
            self.handle_test(test)

    def handle_test(self, test):
        """
        Excecute the test.

        :param test:
        :return:
        """
        driver = self.driver
        params = self.city + "=" + test[self.city] + "&"
        params += self.district + "=" + test[self.district] + "&"
        params += self.street_zone + "=" + test[self.street_zone]
        driver.get(base_url + "show?" + params)
        time.sleep(1)
        if test["location_correct"]:
            # find the successful box
            driver.find_element_by_id(self.location_correct)

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
