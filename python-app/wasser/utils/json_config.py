"""
Django settings class for the project.

Original file copied from Detlef Kreuz Hochschule Heilbronn Project das

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import errno
import json
import os


class JsonConfig:
    """Allow to override settings by external configuration."""

    def __init__(self, config):
        """Initialize config with dictionary."""
        self._config = config

    @classmethod
    def read(cls, envvar='CONFIG_FILE', filename='config/config.json'):
        """Read a JSON configuration file and create a new configuration."""
        filename = os.environ.get(envvar, filename)
        try:
            with open(filename, "r") as config_file:
                config = json.loads(config_file.read())
        except OSError as err:
            if err.errno == errno.ENOENT:
                config = {}
        return cls(config)

    def get(self, key, default):
        """Retrieve settings value for a given key."""
        value = os.environ.get(key)
        if value:
            return value
        return self._config.get(key, default)

    def get_bool(self, key, default):
        """Retrieve boolean settings value."""
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        return value.lower() in ('true', 't', 'yes', 'y')

    def get_list(self, key, default):
        """Get a list in a settings."""
        value = self.get(key, default)
        if isinstance(value, list):
            return value
        return [value]
