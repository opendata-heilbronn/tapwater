"""
tapwater views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import (redirect,
                              render,
                              reverse, get_object_or_404)
from django.core import serializers


from wasser.tapwater.models import (AverageMeasurementValue,
                                    MineralWater,
                                    NutrientDailyDosis)
from wasser.users.models import Measurement, Location
from wasser.tapwater.utilities import (get_zone_data,
                                       prepare_chart_data,
                                       get_last_zone_data)

# Limit for hiding zones on streetzones select box
STREET_ZONE_LIMIT = 100


def index(request):
    """
    Show the main page of tapwater.

    :param request: Http request
    :return: render template tapwater index
    """
    nutrient_daily_dosis = NutrientDailyDosis.objects.get(pk=1)

    mineral_waters = MineralWater.objects.order_by('name')

    average_measurement_value = AverageMeasurementValue.objects.get(pk=1)
    return render(request, 'tapwater/index.html',
                  {"nutrient_daily_dosis": nutrient_daily_dosis,
                   "mineral_waters": mineral_waters,
                   "average_values": average_measurement_value})


def load_tapwater_locations(request):
    """
    Load all districts, which belongs to the selected city.

    :param request: Http request
    :return: HttpResponse with a dumped json
    """
    # load the districts
    if "city" in request.GET and "district" not in request.GET:
        districts = Measurement.objects.filter(
            location__city=request.GET["city"]
        ).values_list('location__district', flat=True).annotate(
            dcount=Count('location__district')
        ).order_by("location__district")
        data = {"districts": list(districts)}
        return JsonResponse(data)

    # load the streetzones
    if "city" in request.GET and "district" in request.GET\
            and "street" not in request.GET and "zone" not in request.GET:
        zones = Measurement.objects.exclude(
            location__street__exact="", location__zone__exact=""
        ).filter(
            location__city=request.GET["city"],
            location__district=request.GET["district"]
        ).values('location__street', 'location__zone').annotate(
            dcount=Count('location__street', 'location__zone')
        ).order_by("location__zone")
        data = {
            "zones": list(zones),
            "street_zone_limit": STREET_ZONE_LIMIT
        }
        return JsonResponse(data)

    return redirect(reverse('index'))


def show_tapwater_values(request):
    """Load values for tapwater."""
    # finally load the measurement values
    if "city" in request.GET:
        street = ""
        district = ""
        zone = ""
        city = request.GET["city"]
        if "district" in request.GET:
            district = request.GET["district"]

        if "streetZone" in request.GET:
            street_zone = request.GET["streetZone"]
            if "|" in street_zone:
                street_zone = street_zone.split("|")
                street = street_zone[1]
                zone = street_zone[0]

        zone_data = get_zone_data(city, district, street, zone)
        chart_data = prepare_chart_data(zone_data)

        nutrient_daily_dosis = get_object_or_404(NutrientDailyDosis, pk=1)
        mineral_waters = MineralWater.objects.order_by('name')
        average_measurement_value = get_object_or_404(AverageMeasurementValue,
                                                      pk=1)

        json_serializer = serializers.get_serializer("json")()

        return render(request, 'tapwater/show_values.html',
                      {"nutrient_daily_dosis": nutrient_daily_dosis,
                       "mineral_waters": mineral_waters,
                       "mineral_waters_json":
                           json_serializer.serialize(mineral_waters),
                       "average_values": average_measurement_value,
                       "street_zone_limit": STREET_ZONE_LIMIT,
                       "zone_data": list(zone_data),
                       "street": street,
                       "zone_data_last": get_last_zone_data(zone_data),
                       "chart_data": chart_data}, )
    return redirect(reverse("index"))


def auto_complete_search_cities(request):
    """Autocomplete search function for cities."""
    if "term" in request.GET:
        term = request.GET["term"].strip()
        cities = Location.objects.values("city")\
            .filter(city__icontains=term)\
            .annotate(dcount=Count('city')).order_by("city")
        return JsonResponse({'cities': list(cities)})
    return redirect(reverse('index'))
