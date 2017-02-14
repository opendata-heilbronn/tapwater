"""
Selenium test for import measurements.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import unittest
import time
from selenium import webdriver
from tests_selenium.utilities import login_admin
from tests_selenium.settings import admin_url


class SendLoginToken(unittest.TestCase):
    """Selenium test for measurement imports."""

    def setUp(self):
        """
        Set up driver.

        :return:
        """
        self.driver = webdriver.Firefox()

    def test_send_token_for_selected_users(self):
        """
        Setup test cases and login as admin.

        :return:
        """
        login_admin(self.driver)  # at first login as admin
        send_login_token_tests = [
            {
                "manipulate_dom": False,
                "user_ids": [1, ],
                "successful": bool(True)
            },
            {
                "manipulate_dom": False,
                "user_ids": [1, 2],
                "successful": bool(True)
            },
            {
                "manipulate_dom": True,
                "user_ids": [99999, ],
                "successful": bool(False)
            },
            {
                "manipulate_dom": False,
                "user_ids": [],
                "successful": str("warning")
            }
        ]

        self.handle_send_token_for_selected_users(send_login_token_tests)

    def handle_send_token_for_selected_users(self, tests):
        """
        Handle Test and evaluate.

        :param tests:
        :return:
        """
        for test in tests:
            # open table with users
            self.driver.get(admin_url + "token/send/selected/")

            for user_id in test["user_ids"]:
                send_token_id = "sendToken" + str(user_id)
                if test["manipulate_dom"]:
                    self.driver.execute_script(
                        "document.getElementById('sendToken1').value='" +
                        str(user_id) + "'")
                    self.driver.find_element_by_id("sendToken1").click()
                else:
                    self.driver.find_element_by_id(send_token_id).click()

            self.driver.find_element_by_id("submitSendToken").click()
            time.sleep(1)
            # evaluate
            if test["successful"] == "warning":
                self.driver.find_element_by_id("send-warning")
                continue

            if bool(test["successful"]) and \
                    type(test["successful"] == bool):
                self.driver.find_element_by_id("send-successful")
                continue

            if not bool(test["successful"]) and \
                    type(test["successful"] == bool):
                self.driver.find_element_by_id("send-failure")
                continue

    def tearDown(self):
        """
        Close driver.

        :return:
        """
        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
