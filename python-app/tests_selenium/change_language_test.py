"""
Selenium test for import measurements.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
from selenium import webdriver

from tests_selenium.settings import base_url


class ChangeLanguage(unittest.TestCase):
    """Selenium test for measurement imports."""

    language_english_id = "language_en"
    language_german_id = "language_de"

    def setUp(self):
        """
        Set up driver.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_change_language(self):
        """
        Define the tests.

        :return:
        """
        driver = self.driver
        driver.get(base_url + "de/")
        driver.find_element_by_id("language_en").click()
        driver.implicitly_wait(5)
        driver.find_element_by_id("language_de").click()
        driver.implicitly_wait(5)
        driver.close()

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
