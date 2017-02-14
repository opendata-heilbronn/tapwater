"""
test for users views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""
import os
from django.test import TestCase
from wasser.utils import json_config


class JsonConfigTest(TestCase):
    """Unit test class for utils json config."""

    def test_json_config_file_exists(self):
        """
        Test json config with a valid file.

        :return:
        """
        os.environ["CONFIG_FILE"] = "config/example-config.json"

        # read existing file
        config = json_config.JsonConfig.read()
        # check reading worked
        host = config.get("DATABASE_HOST", "no_database_host")
        self.assertTrue('localhost' in host)

    def test_json_config_file_not_exists(self):
        """
        Test json config with no valid file.

        :return:
        """
        os.environ["CONFIG_FILE"] = "config/example.json"

        # read existing file
        config = json_config.JsonConfig.read()
        # check reading worked
        host = config.get("DATABASE_HOST", "no_database_host")
        self.assertTrue('no_database_host' in host)

        os.environ["CONFIG_FILE"] = "configgg/example.json"
        # check reading worked
        host = config.get("DATABASE_HOST", "no_database_host")
        self.assertTrue('no_database_host' in host)

    def test_json_config_get(self):
        """
        Test all get methods for json config.

        :return:
        """
        os.environ["CONFIG_FILE"] = "config/example-config.json"

        # read existing file
        config = json_config.JsonConfig.read()
        host = config.get("DATABASE_HOST", "no_database_host")
        self.assertTrue('localhost' in host)

        os.environ["test"] = "test"
        test = config.get("test", "")
        self.assertTrue('test' in test)

        # test with correct value
        google_api = config.get_bool("USE_GOOGLE_API", True)
        self.assertFalse(google_api)

        # test with wrong value
        name = config.get_bool("DATABASE_NAME", True)
        self.assertFalse(name)

        # test with correct value
        allowed_hosts = config.get_list("ALLOWED_HOSTS", [])
        self.assertTrue(len(allowed_hosts) == 2)

        # test with wrong value, list should be returned
        database_user = config.get_list("DATABASE_USER", [])
        self.assertTrue(len(database_user) == 1)
