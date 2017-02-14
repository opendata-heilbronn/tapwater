"""
Selenium test for footer-contents(#84).

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
from selenium import webdriver
from tests_selenium.settings import admin_url, users_url, login_url, base_url
from tests_selenium.utilities import login_admin


class ErrorPage(unittest.TestCase):
    """
    Test class for Info site.

    :return:
    """

    error_actions_id = "error_actions"

    def setUp(self):
        """
        Set up selenium test.

        :return:
        """
        self.base_url = (base_url + "/de/")
        self.driver = webdriver.Firefox()

    def test_error_page(self):
        """
        Test 404 error page.

        :return:
        """
        driver = self.driver
        driver.get(base_url)
        time.sleep(1)
        driver.get(base_url + "123")
        time.sleep(1)
        driver.find_element_by_id("error_actions").click()
        time.sleep(1)
        driver.get(admin_url)
        login_admin(self.driver)
        driver.get(admin_url + "measurement/import/3421+#")
        time.sleep(1)
        driver.find_element_by_id("error_actions").click()
        time.sleep(1)
        driver.get(users_url)
        time.sleep(1)
        driver.get(users_url + "@123")
        time.sleep(1)
        driver.find_element_by_id("error_actions").click()
        time.sleep(1)
        driver.get(login_url)
        time.sleep(1)
        driver.get(login_url + "@1213")
        time.sleep(1)
        driver.find_element_by_id("error_actions").click()
        time.sleep(1)

    def tearDown(self):
        """
        Close the driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
