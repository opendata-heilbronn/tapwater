"""
Selenium test for insert measurement.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
from selenium import webdriver
from tests_selenium.settings import users_url
from tests_selenium.utilities import login_user


class InsertMeasurement(unittest.TestCase):
    """Test Class for insert measurement."""

    city = "city"
    district = "district"
    region = "region"
    date = "date"
    source = "source"
    remarks = "remarks"

    sodium = "sodium"
    potassium = "potassium"
    calcium = "calcium"
    magnesium = "magnesium"
    chloride = "chloride"
    nitrate = "nitrate"
    sulfate = "sulfate"
    degree_of_hardness = "degree_of_hardness"

    street = "street"
    zone = "zone"

    save_successful_id = "save-successful"
    save_failed_id = "save-failed"
    add_new_zone_id = "add_new_zone"
    send_values_id = "send_values"

    def setUp(self):
        """
        Set up selenium test.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_insert_measurement(self):
        """
        Create the test measurements as list.

        :return:
        """
        insert_measurement_tests = [
            {
                self.city: "Heilbronn",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": True
            },
            {
                self.city: "Heilbronn",
                self.district: "",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": True
            },
            {
                self.city: "Heilbronn",
                self.district: "",
                self.date: "12.12.2015",
                self.region: "Heilbronn",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: [""],
                self.zone: [""],
                "successful": True
            },
            {  # test with two zones
                self.city: "Heilbronn",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: ["Schwaigener str.", "Test Strasse"],
                self.zone: ["Westzone"],
                "successful": True
            },
            {  # test with two zones
                self.city: "Heilbronn",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "",
                self.remarks: "2mal angefragt",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: ["Schwaigener str.", "Test Strasse"],
                self.zone: ["Westzone"],
                "successful": True
            },
            {  # test with two zones
                self.city: "Heilbronn",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "",
                self.remarks: "",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: ["Schwaigener str.", "Test Strasse"],
                self.zone: ["Westzone"],
                "successful": True
            },
            {  # test with two zones
                self.city: "Heilbronn",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "",
                self.source: "",
                self.remarks: "",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: ["Schwaigener str.", "Test Strasse"],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "",
                self.potassium: "",
                self.calcium: "",
                self.magnesium: "",
                self.sulfate: "",
                self.nitrate: "",
                self.chloride: "",
                self.degree_of_hardness: "",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "1.0",
                self.potassium: "",
                self.calcium: "",
                self.magnesium: "",
                self.sulfate: "",
                self.nitrate: "",
                self.chloride: "",
                self.degree_of_hardness: "",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "",
                self.potassium: "1.0",
                self.calcium: "",
                self.magnesium: "",
                self.sulfate: "",
                self.nitrate: "",
                self.chloride: "",
                self.degree_of_hardness: "",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "",
                self.potassium: "",
                self.calcium: "1.0",
                self.magnesium: "",
                self.sulfate: "",
                self.nitrate: "",
                self.chloride: "",
                self.degree_of_hardness: "",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "",
                self.potassium: "",
                self.calcium: "",
                self.magnesium: "1.0",
                self.sulfate: "",
                self.nitrate: "",
                self.chloride: "",
                self.degree_of_hardness: "",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "",
                self.potassium: "",
                self.calcium: "",
                self.magnesium: "",
                self.sulfate: "1.0",
                self.nitrate: "",
                self.chloride: "",
                self.degree_of_hardness: "",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "",
                self.potassium: "",
                self.calcium: "",
                self.magnesium: "",
                self.sulfate: "",
                self.nitrate: "1.0",
                self.chloride: "",
                self.degree_of_hardness: "",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "",
                self.potassium: "",
                self.calcium: "",
                self.magnesium: "",
                self.sulfate: "",
                self.nitrate: "",
                self.chloride: "1.00",
                self.degree_of_hardness: "",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "",
                self.district: "Niederhofen",
                self.region: "Heilbronn",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "",
                self.potassium: "",
                self.calcium: "",
                self.magnesium: "",
                self.sulfate: "",
                self.nitrate: "",
                self.chloride: "",
                self.degree_of_hardness: "1.0",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },
            {
                self.city: "Heilbronn",
                self.district: "Niederhofen",
                self.region: "",
                self.date: "12.12.2015",
                self.source: "wikipedia",
                self.remarks: "2mal angefragt",
                self.sodium: "1.5",
                self.potassium: "1.44",
                self.calcium: "1.888",
                self.magnesium: "1.12",
                self.sulfate: "1.10",
                self.nitrate: "1.00",
                self.chloride: "10.0",
                self.degree_of_hardness: "0.1",
                self.street: ["Schwaigener str."],
                self.zone: ["Westzone"],
                "successful": False
            },

        ]

        login_user(self.driver)
        for test in insert_measurement_tests:
            self.handle_test(test)

    def handle_test(self, test):
        """
        Excecute the test.

        :param test:
        :return:
        """
        driver = self.driver
        driver.get(users_url + "measurement/insert/")
        city = driver.find_element_by_name(self.city)
        city.send_keys(test[self.city])
        district = driver.find_element_by_name(self.district)
        district.send_keys(test[self.district])
        region = driver.find_element_by_name(self.region)
        region.send_keys(test[self.region])
        year = driver.find_element_by_name(self.date)
        year.send_keys(test[self.date])
        source = driver.find_element_by_name(self.source)
        source.send_keys(test[self.source])
        remarks = driver.find_element_by_name(self.remarks)
        remarks.send_keys(test[self.remarks])
        sodium = driver.find_element_by_name(self.sodium)
        sodium.send_keys(test[self.sodium])
        potassium = driver.find_element_by_name(self.potassium)
        potassium.send_keys(test[self.potassium])
        calcium = driver.find_element_by_name(self.calcium)
        calcium.send_keys(test[self.calcium])
        magnesium = driver.find_element_by_name(self.magnesium)
        magnesium.send_keys(test[self.magnesium])
        sulfate = driver.find_element_by_name(self.sulfate)
        sulfate.send_keys(test[self.sulfate])
        degree_of_hardness = \
            driver.find_element_by_name(self.degree_of_hardness)
        degree_of_hardness.send_keys(test[self.degree_of_hardness])
        chloride = driver.find_element_by_name(self.chloride)
        chloride.send_keys(test[self.chloride])
        nitrate = driver.find_element_by_name(self.nitrate)
        nitrate.send_keys((test[self.nitrate]))

        # count the number of given zones
        number_of_zones = len(test[self.street])
        if number_of_zones > 1:
            for x in (1, number_of_zones):
                driver.find_element_by_id(self.add_new_zone_id).click()
            pass

        counter = 1  # Define counter for street
        for value in test[self.street]:
            street = driver.find_element_by_name(self.street + str(counter))
            street.send_keys(value)
            counter += 1
            pass

        counter = 1  # reset counter for zones
        for value in test[self.zone]:
            zone = driver.find_element_by_name(self.zone + str(counter))
            zone.send_keys(value)
            counter += 1
            pass

        # find the send button
        driver.find_element_by_id(self.send_values_id).click()

        time.sleep(1)
        if test["successful"]:
            # find the successful box
            driver.find_element_by_id(self.save_successful_id)

        if not test["successful"]:
            # find the failed box
            driver.find_element_by_id(self.save_failed_id)

    def tearDown(self):
        """
        Close the driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
