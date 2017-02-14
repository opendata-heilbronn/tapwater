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


class InfoSite(unittest.TestCase):
    """
    Test class for Info site.

    :return:
    """

    def setUp(self):
        """
        Set up selenium test.

        :return:
        """
        self.base_url = base_url
        self.driver = webdriver.Firefox()

    def test_footer_tapwater(self):
        """
        Click on tapwater area.

        :return:
        """
        driver = self.driver
        driver.get(base_url)
        elements = driver.find_elements_by_css_selector(
            "footer.footer a.footer-link")
        for element in elements:
            element.click()
            time.sleep(1)
            driver.find_element_by_css_selector(
                "div.modal.fade.in button.close").click()
            time.sleep(1)
        time.sleep(1)

    def test_footer_admin(self):
        """
        Click on admin area.

        :return:
        """
        driver = self.driver
        driver.get(admin_url)
        elements = driver.find_elements_by_css_selector(
            "footer.footer a.footer-link")
        for element in elements:
            element.click()
            time.sleep(1)
            driver.find_element_by_css_selector(
                "div.modal.fade.in button.close").click()
            time.sleep(1)
        time.sleep(1)

    def test_footer_login(self):
        """
        Click on login area.

        :return:
        """
        driver = self.driver
        driver.get(login_url)
        elements = driver.find_elements_by_css_selector(
            "footer.footer a.footer-link")
        for element in elements:
            element.click()
            time.sleep(1)
            driver.find_element_by_css_selector(
                "div.modal.fade.in button.close").click()
            time.sleep(1)
        time.sleep(1)

    def test_footer_users(self):
        """
        Click on users area.

        :return:
        """
        driver = self.driver
        driver.get(users_url)
        elements = driver.find_elements_by_css_selector(
            "footer.footer a.footer-link")
        for element in elements:
            element.click()
            time.sleep(1)
            driver.find_element_by_css_selector(
                "div.modal.fade.in button.close").click()
            time.sleep(1)
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
