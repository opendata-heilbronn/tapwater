"""
tapwater models.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import datetime

from django.db import models
from wasser.administration.models import TapwaterUser


class Location(models.Model):
    """Model for measurement location."""

    city = models.CharField(max_length=100, blank=False)
    region = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    zone = models.CharField(max_length=100, blank=True)

    def validate_model(self):
        """
        Validate required fields in model.

        :return:
        """
        if self.city.strip() == "" or self.region.strip() == "":
            return False
        self.save()
        return True


class Minerals(models.Model):
    """Model for measurement minerals."""

    sodium = models.CharField(max_length=100)  # natrium
    potassium = models.CharField(max_length=100)  # kalium
    calcium = models.CharField(max_length=100)
    magnesium = models.CharField(max_length=100)
    chloride = models.CharField(max_length=100)
    nitrate = models.CharField(max_length=100)
    sulfate = models.CharField(max_length=100)

    def validate_model(self):
        """
        Validate only minerals.

        :return:
        """
        if self.sodium.strip() == "" or \
                self.potassium.strip() == "" or \
                self.calcium.strip() == "" or \
                self.sodium.strip() == "":
            return False

        if self.magnesium.strip() == "" or \
                self.chloride.strip() == "" or \
                self.nitrate.strip() == "" or \
                self.sulfate.strip() == "" or \
                self.sodium.strip() == "":
            return False
        self.save()
        return True


class Measurement(models.Model):
    """Basis model for measurements which contains all values."""

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    minerals = models.ForeignKey(Minerals, on_delete=models.CASCADE)
    user = models.ForeignKey(TapwaterUser, on_delete=models.SET_NULL,
                             null=True)
    created = models.DateTimeField(auto_now_add=True)
    hardness = models.CharField(max_length=100)  # haertegrad
    date = models.CharField(max_length=10)
    remarks = models.TextField()
    source = models.TextField()

    def add_measurement(self):
        """
        Add a measurement to database after validating it.

        :return:
        """
        if self.validate_model():
            self.save()
            return True
        return False

    def validate_model(self):
        """
        Validate model values.

        :return: false on error
        """
        if str(self.date).strip() == "" or \
                self.hardness.strip() == "":
            return False

        try:
            datetime.datetime.strptime(self.date, '%d.%m.%Y')
        except ValueError:
            return False

        return True
