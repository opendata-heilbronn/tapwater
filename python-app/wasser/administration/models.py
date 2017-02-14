
"""
Administration models.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import json
import csv

from django.conf import settings
from django.db import models


class TapwaterUserType(models.Model):
    """Model for user typ."""

    value = models.TextField(max_length=100)


class TapwaterUser(models.Model):
    """Model for users."""

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=False, blank=False)

    authority = models.CharField(max_length=100)
    type = models.ForeignKey(TapwaterUserType,
                             on_delete=models.SET_NULL,
                             null=True)
    verified = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)


class ImportMeasurementsDocument(models.Model):
    """Model for upload documents."""

    locations = models.FileField(upload_to='documents/%Y/%m/%d', blank=False)
    zones = models.FileField(upload_to='documents/%Y/%m/%d', blank=False)
    selenium_test_dir = "/code/tests_selenium/testdata/"
    jenkins_workspace = "/var/lib/jenkins/jobs/Wasser/workspace/tests_selenium"

    def load_location_json(self):
        """
        Load file location.json from document root.

        :return:
        """
        filename = self.locations.name
        filepath = settings.MEDIA_ROOT + '/' + filename
        # Use files from testdata folder for tests.
        if filename.startswith(self.selenium_test_dir) | \
                filename.startswith(self.jenkins_workspace):
            filepath = filename
        try:
            with open(filepath, encoding='utf-8') as json_data:
                data_locations = json.load(json_data)
                if 'Locations' not in data_locations:
                    return False
        except ValueError:
            return False
        return data_locations

    def load_zone_json(self):
        """
        Load file zone.json from document root.

        :return:
        """
        filename = self.zones.name
        filepath = settings.MEDIA_ROOT + '/' + filename
        # Use files from testdata folder for tests.
        if filename.startswith(self.selenium_test_dir) | \
                filename.startswith(self.jenkins_workspace):
            filepath = filename
        try:
            with open(filepath, encoding='utf-8') as json_data:
                data_zones = json.load(json_data)
        except ValueError:
            return False
        return data_zones

    def is_valid_json_location(self):
        """
        Check if location.json is valid.

        :return:
        """
        try:
            filename = self.locations.name
            filepath = settings.MEDIA_ROOT + '/' + filename
            if filename.startswith(self.selenium_test_dir) | \
                    filename.startswith(self.jenkins_workspace):
                filepath = filename
            with open(filepath, encoding='utf-8') as json_data:
                locations = json.load(json_data)
                if 'Locations' not in locations:
                    return False
        except ValueError:
            return False
        return True

    def is_valid_json_zone(self):
        """
        Check if zone.json is valid.

        :return:
        """
        try:
            filename = self.zones.name
            filepath = settings.MEDIA_ROOT + '/' + filename
            if filename.startswith(self.selenium_test_dir) | \
                    filename.startswith(self.jenkins_workspace):
                filepath = filename
            with open(filepath, encoding='utf-8') as json_data:
                zones = json.load(json_data)
                if 'Zones' not in zones:
                    return False
        except ValueError:
            return False
        return True


class ImportContactsDocument(models.Model):
    """Model for upload contact documents (csv)."""

    contacts = models.FileField(upload_to='contacts/%Y/%m/%d', blank=False)
    selenium_test_dir = "/code/tests_selenium/testdata/"
    jenkins_workspace = "/var/lib/jenkins/jobs/Wasser/workspace/tests_selenium"

    def is_valid_csv(self):
        """
        Check if contacts.csv is valid.

        :return:
        """
        try:
            filename = self.contacts.name
            filepath = settings.MEDIA_ROOT + '/' + filename
            if filename.startswith(self.selenium_test_dir) | \
                    filename.startswith(self.jenkins_workspace):
                filepath = filename
            with open(filepath) as csv_data:
                reader = csv.DictReader(csv_data, dialect=csv.excel,
                                        delimiter=';', skipinitialspace=True)
                for row in reader:
                    if not len(row) == 4:
                        return False
                    for column in ['Vorname', 'Nachname', 'Mail', 'Gemeinde']:
                        if column not in row:
                            return False
                    if "@" not in row["Mail"]:
                        return False
        except UnicodeDecodeError:
            return False
        return True

    def load_contacts_csv(self):
        """
        Load file contacts csv from contacts root.

        :return:
            csv_data_list: list with the elements of the CSV-File
        """
        try:
            filename = self.contacts.name
            filepath = settings.MEDIA_ROOT + '/' + filename
            if filename.startswith(self.selenium_test_dir) | \
                    filename.startswith(self.jenkins_workspace):
                filepath = filename
            with open(filepath) as csv_data:
                csv_reader = csv.reader(csv_data, dialect=csv.excel,
                                        delimiter=';', skipinitialspace=True)
                next(csv_reader, None)
                csv_data_list = list(csv_reader)
        except ValueError:
            return False
        return csv_data_list


class Token(models.Model):
    """Token class for users login."""

    valid_until = models.DateField()
    value = models.CharField(max_length=60)
    user_id = models.CharField(max_length=100)
