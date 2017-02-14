"""
Selenium test for import measurements.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
from selenium import webdriver
from tests_selenium.settings import admin_url
from tests_selenium.utilities import login_admin, set_form_novalidate


class EditMineralWater(unittest.TestCase):
    """Selenium test for measurement imports."""

    potassium = "potassium"
    sodium = "sodium"
    calcium = "calcium"
    magnesium = "magnesium"
    chloride = "chloride"
    nitrate = "nitrate"
    sulfate = "sulfate"
    key = "key"
    name = "name"
    sources = "sources"

    save_successful_id = "save-successful"
    save_failed_id = "save-failed"

    send_values_id = "send_values"

    def setUp(self):
        """
        Setup selenium test.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_edit_mineral_water(self):
        """
        Define the tests.

        :return:
        """
        change_measurement_tests = [
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": True
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "13.6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "11,8",
                self.sodium: "2,9",
                self.calcium: "49,9",
                self.magnesium: "14,3",
                self.chloride: "12",
                self.nitrate: "13",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "",
                self.sources: "www.google.de",
                self.potassium: "11,8",
                self.sodium: "2,9",
                self.calcium: "49,9",
                self.magnesium: "14,3",
                self.chloride: "12",
                self.nitrate: "13",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "",
                self.sulfate: "49",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "teusser",
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "",
                "successful": False
            },
            {
                self.name: "Teusser",
                self.key: "volvic",
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "",
                "successful": False
            }
        ]

        login_admin(self.driver)

        for test in change_measurement_tests:
            self.handle_edit_test(test)

    def test_go_back(self):
        """
        Execute go back Test.

        :return:
        """
        login_admin(self.driver)
        driver = self.driver
        driver.get(admin_url + "mineral_waters/edit/2/")
        driver.find_element_by_id("btnBack").click()

    def handle_edit_test(self, test):
        """
        Excecute test.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(admin_url + "mineral_waters/edit/2/")

        # edit form
        set_form_novalidate(driver, "formEditMineralWater")

        name = driver.find_element_by_name(self.name)
        name.clear()
        name.send_keys(test[self.name])
        key = driver.find_element_by_name(self.key)
        key.clear()
        key.send_keys(test[self.key])
        sources = driver.find_element_by_name(self.sources)
        sources.clear()
        sources.send_keys(test[self.sources])
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

        driver.find_element_by_id(self.send_values_id).click()
        driver.implicitly_wait(5)

        if test["successful"]:
            driver.find_element_by_id("save-successful")

        if not test["successful"]:
            driver.find_element_by_id("save-failure")

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
