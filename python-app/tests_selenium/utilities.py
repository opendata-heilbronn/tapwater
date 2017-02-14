"""
Selenium test for import measurements.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""
import time
from tests_selenium.settings import base_url

user_id = 1
user_token = "d1d26d4aa203450d9492bf84fa9c3762"

admin_user = "admin"
admin_password = "AdminWasser"


def login_user(driver):
    """Login as Selenium user for testing."""
    driver.get(base_url + "login/authority/?id=" + str(user_id)
               + "&token=" + user_token)
    time.sleep(1)


def login_admin(driver):
    """Login as Admin user for testing."""
    driver.get(base_url + "login/admin/")
    driver.find_element_by_id("user").send_keys(admin_user)
    driver.find_element_by_id("password").send_keys(admin_password)
    driver.find_element_by_id("submit").click()
    time.sleep(1)


def set_form_novalidate(driver, id_form):
    """Set novalidate for forms on selenium test."""
    novalidate = "document.getElementById('" + id_form + "')." \
                 "noValidate = true;"
    driver.execute_script(novalidate)
