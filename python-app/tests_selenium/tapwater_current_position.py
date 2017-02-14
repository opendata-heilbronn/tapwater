"""
Selenium test for tapwater geolocate.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import os
import time
import unittest

from selenium import webdriver

from selenium.webdriver.support.ui import Select


class TapwaterStreetZones(unittest.TestCase):
    """Selenium test for measurement imports."""

    def setUp(self):
        """
        Setup selenium test.

        :return:
        """
        self.base_url = "http://localhost:8000/"
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("geo.prompt.testing", True)
        self.profile.set_preference("geo.prompt.testing.allow", True)

    def test_get_current_position(self):
        """
        Check if geolocation is the expected.

        :return:
        """
        fake_position_json = os.path.abspath('testdata/fake_grantschen.json')
        fake_position_json_path = 'file:///' + fake_position_json
        # Give Firefox the Fake-Geoposition
        self.profile.set_preference("geo.wifi.uri", fake_position_json_path)
        self.driver = webdriver.Firefox(self.profile)
        self.driver.get(self.base_url)
        self.driver.find_element_by_id('locateUser').click()

        select = Select(self.driver.find_element_by_id('city'))
        selected_city = select.first_selected_option.get_attribute("value")
        time.sleep(5)

        select2 = Select(self.driver.find_element_by_id('district'))
        selected_district = select2.first_selected_option\
            .get_attribute("value")
        time.sleep(2)

        if selected_city != "Weinsberg" and selected_district != "Grantschen":
            self.fail("No such element found")

    def test_wrong_position(self):
        """
        Check if geolocation is correct.

        :return:
        """
        fake_position_json = os.path.abspath('testdata/fake_berlin.json')
        fake_position_json_path = 'file:///' + fake_position_json
        # Give Firefox the Fake-Geoposition
        self.profile.set_preference("geo.wifi.uri", fake_position_json_path)
        self.driver = webdriver.Firefox(self.profile)
        self.driver.get(self.base_url)
        self.driver.find_element_by_id('locateUser').click()
        time.sleep(4)
        info_text = self.driver.find_element_by_id('info').text
        if info_text == "":
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
