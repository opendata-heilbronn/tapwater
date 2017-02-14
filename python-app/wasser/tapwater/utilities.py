"""
tapwater utilities.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import json
from django.db.models import F
from django.db.models import Count

from wasser.users.models import Measurement


def get_zone_data(city, district, street, zone):
    """Get Zone data for show_values."""
    zone_data = Measurement.objects.filter(
        location__city=city,
        location__district=district,
        location__street=street,
        location__zone=zone
    ).values(
        'minerals__sodium', 'minerals__potassium', 'hardness',
        'minerals__calcium', 'minerals__magnesium',
        'minerals__chloride', 'minerals__nitrate', 'minerals__sulfate',
        'date', 'remarks', 'id', 'user__lastname', 'user__type__value',
        'user__verified', 'created', 'user__authority', 'user__id',
        'user__registration_date'
    ).annotate(sodium=F('minerals__sodium'),
               potassium=F('minerals__potassium'),
               calcium=F('minerals__calcium'),
               magnesium=F('minerals__magnesium'),
               chloride=F('minerals__chloride'),
               nitrate=F('minerals__nitrate'),
               sulfate=F('minerals__sulfate'),
               dcount=Count('date'),
               username=F('user__lastname')).order_by('-date', '-created')
    return zone_data


def get_last_zone_data(zone_data):
    """Get last zone data and prepare the remarks value."""
    last_zone_data = list()
    if len(zone_data) > 0:
        last_zone_data = list(zone_data)[0]
        last_zone_data["remarks"] = last_zone_data["remarks"]\
            .replace('\n', ' ').replace('\r', '').replace("'", '')
    return last_zone_data


def prepare_chart_data(zone_data):
    """Prepare data for chart history."""
    chart_data = []
    for data in zone_data:
        obj = dict()
        obj["sodium"] = data["minerals__sodium"]
        obj["calcium"] = data["minerals__calcium"]
        obj["potassium"] = data["minerals__potassium"]
        obj["sulfate"] = data["minerals__sulfate"]
        obj["chloride"] = data["minerals__chloride"]
        obj["nitrate"] = data["minerals__nitrate"]
        obj["magnesium"] = data["minerals__magnesium"]
        obj["hardness"] = data["hardness"]
        obj["date"] = data["date"]
        chart_data.insert(0, obj)

    return json.dumps(chart_data)
