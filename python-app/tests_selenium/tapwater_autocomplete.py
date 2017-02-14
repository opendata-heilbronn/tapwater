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

    term = "term"
    city = "city"

    continue_button_id = "btnContinue"
    search_button_id = "search"
    locate_user_button_id = "locateUser"
    share_link_button_id = "shareLinkButton"
    no_values_found_div = "noValuesFound"

    def setUp(self):
        """
        Set up driver.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_find_required_elements(self):
        """
        Find all required elements for this test.

        :return:
        """
        self.driver.get(base_url)
        self.driver.find_element_by_id(self.city)
        self.driver.find_element_by_id(self.continue_button_id)
        self.driver.find_element_by_id(self.search_button_id)
        self.driver.find_element_by_id(self.locate_user_button_id)

    def test_city_autocomplete_correct_value(self):
        """
        Test autocomplete with correct term for city.

        :return:
        """
        self.handle_test("He", "Heilbronn")
        self.handle_test("a", "Massenbachhausen")
        self.handle_test("bach", "Erlenbach")

    def test_city_autocomplete_wrong_value(self):
        """
        Test autocomplete with wrong term for any city.

        :return:
        """
        self.handle_test("xxx", False)

    def test_autocomplete_redirect(self):
        """Test redirect for autocomplete ajax request without value."""
        self.driver.get(base_url + "autocomplete/cities")
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_id(self.city)
        self.driver.find_element_by_id(self.continue_button_id)
        self.driver.find_element_by_id(self.search_button_id)
        self.driver.find_element_by_id(self.locate_user_button_id)

    def handle_test(self, term, city):
        """
        Excecute the test. Handle success when shared values are there.

        :param term: search term
        :param city: city we search for
        :return:
        """
        driver = self.driver
        driver.get(base_url)
        city_input = driver.find_element_by_id(self.city)
        city_input.send_keys(term)
        time.sleep(1)

        autocomplete_ul = driver.find_element_by_css_selector(
            "ul.ui-autocomplete")
        li_items = autocomplete_ul.find_elements_by_tag_name("li")
        for item in li_items:
            if item.text == city:
                item.click()
                time.sleep(1)
                break

        driver.find_element_by_id(self.search_button_id).click()
        driver.implicitly_wait(2)
        city_input.send_keys(u'\ue007')
        time.sleep(1)
        if city:
            driver.find_element_by_id(self.share_link_button_id)
        else:
            driver.find_element_by_id(self.no_values_found_div)

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
