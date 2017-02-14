"""
tapwater models.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.db import models
from django.urls import reverse


class MineralWater(models.Model):
    """Model for different mineral waters."""

    name = models.CharField(max_length=100, blank=False, null=False)
    key = models.CharField(max_length=100, blank=False, null=False)
    sodium = models.CharField(max_length=50)
    potassium = models.CharField(max_length=50)
    calcium = models.CharField(max_length=50)
    magnesium = models.CharField(max_length=50)
    chloride = models.CharField(max_length=50)
    nitrate = models.CharField(max_length=50)
    sulfate = models.CharField(max_length=50)
    referenced = models.BooleanField()
    sources = models.TextField()


class AverageMeasurementValue(models.Model):
    """Model for avg measurement values."""

    sodium = models.CharField(max_length=50)
    potassium = models.CharField(max_length=50)
    calcium = models.CharField(max_length=50)
    magnesium = models.CharField(max_length=50)
    chloride = models.CharField(max_length=50)
    nitrate = models.CharField(max_length=50)
    sulfate = models.CharField(max_length=50)
    hardness = models.CharField(max_length=50, default='')

    @staticmethod
    def get_absolute_url():
        """Get absolute url."""
        return reverse("show_average_measurement_value")


class NutrientDailyDosis(models.Model):
    """Model for nutrient daily dosis of minerals."""

    potassium = models.CharField(max_length=50)
    calcium = models.CharField(max_length=50)
    magnesium = models.CharField(max_length=50)
