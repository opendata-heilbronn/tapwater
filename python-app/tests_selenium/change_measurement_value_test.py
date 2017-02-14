"""
Selenium test for import measurements.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
from selenium import webdriver
from tests_selenium.settings import admin_url
from tests_selenium.utilities import login_admin


class ChangeMeasurement(unittest.TestCase):
    """Selenium test for measurement imports."""

    potassium = "potassium"
    sodium = "sodium"
    calcium = "calcium"
    magnesium = "magnesium"
    chloride = "chloride"
    nitrate = "nitrate"
    sulfate = "sulfate"
    hardness = "hardness"

    save_successful_id = "save-successful"
    save_failed_id = "save-failed"

    send_values_id = "send_values"
    cancel_values_id = "cancel_change"

    def setUp(self):
        """
        Setup selenium test.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_change_measurement(self):
        """
        Define the tests.

        :return:
        """
        change_measurement_tests = [
             {
                 self.potassium: "13,6",
                 self.sodium: "1,9",
                 self.calcium: "75,0",
                 self.magnesium: "16,1",
                 self.chloride: "19",
                 self.nitrate: "13,6",
                 self.sulfate: "49",
                 self.hardness: "2,0",
                 "successful": True
             },
             {
                self.potassium: "11,8",
                self.sodium: "2,9",
                self.calcium: "49,9",
                self.magnesium: "14,3",
                self.chloride: "12",
                self.nitrate: "13",
                self.sulfate: "",
                self.hardness: "2,0",
                "successful": False

             },
        ]

        login_admin(self.driver)

        for test in change_measurement_tests:
            self.handle_test(test)

    def handle_test(self, test):
        """
        Excecute test.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(admin_url + "average_measurement_value/edit/")

        potassium = driver.find_element_by_name(self.potassium)
        potassium.clear()
        potassium.send_keys(test[self.potassium])
        sodium = driver.find_element_by_name(self.sodium)
        sodium.clear()
        sodium.send_keys(test[self.sodium])
        calcium = driver.find_element_by_name(self.calcium)
        calcium.clear()
        calcium.send_keys(test[self.calcium])
        magnesium = driver.find_element_by_name(self.magnesium)
        magnesium.clear()
        magnesium.send_keys(test[self.magnesium])
        chloride = driver.find_element_by_name(self.chloride)
        chloride.clear()
        chloride.send_keys(test[self.chloride])
        nitrate = driver.find_element_by_name(self.nitrate)
        nitrate.clear()
        nitrate.send_keys(test[self.nitrate])
        sulfate = driver.find_element_by_name(self.sulfate)
        sulfate.clear()
        sulfate.send_keys(test[self.sulfate])
        hardness = driver.find_element_by_name(self.hardness)
        hardness.clear()
        hardness.send_keys(test[self.hardness])

        driver.find_element_by_id(self.send_values_id).click()
        driver.implicitly_wait(5)

        if test["successful"]:
            driver.find_element_by_id("save-successful")

        if not test["successful"]:
            sulfate = driver.find_element_by_name(self.sulfate)
            sulfate.clear()
            sulfate.send_keys("2,5")
            driver.find_element_by_id(self.send_values_id).click()
            driver.implicitly_wait(5)
            driver.find_element_by_id("save-successful")

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
