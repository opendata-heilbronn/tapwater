"""
Selenium test for #103: Delete mineral water.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""
import unittest

from selenium import webdriver
from tests_selenium.settings import admin_url
from tests_selenium.utilities import login_admin, set_form_novalidate


class AddMineralwater(unittest.TestCase):
    """Selenium test for add mineral water."""

    key_to_delete = "sprudel"

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

    send_values_id = "send_values"

    cancel_id = "btnCancel-"
    yes_id = "btnConfirm-"

    def setUp(self):
        """
        Setup selenium test.

        :return:
        """
        self.driver = webdriver.Firefox()

    def handle_add_test(self):
        """
        Excecute test for adding mineral waters.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(admin_url + "mineral_waters/add/")

        add_water_tests = [
            {
                self.name: "Sprudel",
                self.key: self.key_to_delete,
                self.sources: "www.google.de",
                self.potassium: "13,6",
                self.sodium: "1,9",
                self.calcium: "75,0",
                self.magnesium: "16,1",
                self.chloride: "19",
                self.nitrate: "13,6",
                self.sulfate: "49",
                "successful": True
            }
        ]

        test = add_water_tests[0]

        set_form_novalidate(driver, "formAddMineralWater")

        name = driver.find_element_by_name(self.name)
        name.send_keys(test[self.name])

        key = driver.find_element_by_name(self.key)
        key.send_keys(test[self.key])

        sources = driver.find_element_by_name(self.sources)
        sources.send_keys(test[self.sources])

        potassium = driver.find_element_by_name(self.potassium)
        potassium.send_keys(test[self.potassium])

        sodium = driver.find_element_by_name(self.sodium)
        sodium.send_keys(test[self.sodium])

        calcium = driver.find_element_by_name(self.calcium)
        calcium.send_keys(test[self.calcium])

        magnesium = driver.find_element_by_name(self.magnesium)
        magnesium.send_keys(test[self.magnesium])

        chloride = driver.find_element_by_name(self.chloride)
        chloride.send_keys(test[self.chloride])

        nitrate = driver.find_element_by_name(self.nitrate)
        nitrate.send_keys(test[self.nitrate])

        sulfate = driver.find_element_by_name(self.sulfate)
        sulfate.send_keys(test[self.sulfate])

        driver.find_element_by_id(self.send_values_id).click()
        driver.implicitly_wait(5)

        if test["successful"]:
            driver.find_element_by_id("save-successful")

    def test_cancel_delete_water(self):
        """
        Test to delete a created water.

        :return:
        """
        login_admin(self.driver)
        self.handle_add_test()  # add sample water

        driver = self.driver
        driver.get(admin_url + "mineral_waters/show")
        driver.implicitly_wait(2)
        driver.find_element_by_id("delete-mineral-water-" +
                                  self.key_to_delete).click()
        driver.implicitly_wait(2)
        driver.find_element_by_id(self.cancel_id + self.key_to_delete).click()

    def test_delete_water(self):
        """
        Test to delete a created water.

        :return:
        """
        login_admin(self.driver)  # login

        driver = self.driver
        driver.get(admin_url + "mineral_waters/show")
        driver.find_element_by_id("delete-mineral-water-" +
                                  self.key_to_delete).click()
        driver.implicitly_wait(2)
        driver.find_element_by_id(self.yes_id + self.key_to_delete).click()
        driver.implicitly_wait(2)
        driver.find_element_by_id("deleteMessage")  # check successful

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
