"""
Selenium test for tapwater street zones.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
from selenium import webdriver
from tests_selenium.settings import base_url


class TapwaterStreetZones(unittest.TestCase):
    """Selenium test for measurement imports."""

    city = "city"
    district = "district"
    streetZone = "streetZone"

    def setUp(self):
        """
        Set up driver.

        :return:
        """
        self.driver = webdriver.Firefox()
        self.driver.get(base_url)

    def test_has_no_optgroup(self):
        """
        Check steetzone has no optiongroup.

        :return:
        """
        driver = self.driver

        city_box = driver.find_element_by_id(self.city)
        city_box.send_keys("Heilbronn")

        search_button = driver.find_element_by_id("search")
        search_button.click()
        driver.implicitly_wait(5)

        street_box = driver.find_element_by_id(self.streetZone)
        option_groups = street_box.find_elements_by_tag_name('optgroup')
        driver.implicitly_wait(5)

        if len(option_groups) is not 0:
            self.fail("No such element found")

    def test_has_optgroup(self):
        """
        Check steetzone has no optiongroup.

        :return:
        """
        driver = self.driver

        city_box = driver.find_element_by_id(self.city)
        city_box.send_keys("Beilstein")

        search_button = driver.find_element_by_id("search")
        search_button.click()
        driver.implicitly_wait(5)

        street_box = driver.find_element_by_id(self.streetZone)
        option_groups = street_box.find_elements_by_tag_name('optgroup')
        driver.implicitly_wait(5)

        if len(option_groups) is 0:
            self.fail("No such element found")

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
