"""
Administration utilities.

Used for imports.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import collections
import re
import random
import string
import socket

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _

from wasser.users.models import (Measurement, Location,
                                 Minerals)
from wasser.administration.models import (TapwaterUser,
                                          TapwaterUserType)

NOT_INSERT = []


def get_key(city, suburb, zone):
    """
    Creating ea fitting key.

    :param
        city (String): City name
        suburb (String): Suburb name
        zone (String): Zone name
    :return
        key: string with key
    """
    if city != "" and suburb != "" and suburb != city and zone != "":
        key = city + " " + suburb + " " + zone
    elif city != "" and suburb != "" and suburb == city and zone != "":
        key = suburb + " " + zone
    elif city != "" and suburb != "" and suburb == city and zone == "":
        key = suburb
    elif city != "" and suburb != "" and zone == "":
        key = city + " " + suburb
    elif city != "" and suburb == "" and zone != "":
        key = city + " " + zone
    else:
        key = city
    return key


def insert_measurement_to_database(key, value, data_zones, region):
    """
    Try to write data (measurements, city, street etc.) to posgres database.

    :param
        key (String): City name
        value (String): Street name
    """
    try:
        parts = key.split('_')
        if len(parts) == 3:
            city = parts[0]
            suburb = parts[1]
            zone = parts[2]
        elif len(parts) == 2:
            city = parts[0]
            suburb = parts[1]
            zone = ""
        else:
            city = parts[0]
            suburb = ""
            zone = ""

        if zone == '{}':
            zone = ""
        if len(value) == 0:
            value = ""

        source = ""

        key = get_key(city, suburb, zone)

        location_exists = Location()

        if Location.objects.filter(city=str(city).strip(),
                                   district=str(suburb).strip(),
                                   street=str(value).strip(),
                                   zone=str(zone).strip()).exists():
            location_exists = Location.objects.get(
                city=str(city).strip(),
                district=str(suburb).strip(),
                street=str(value).strip(),
                zone=str(zone).strip())

        minerals = Minerals()
        minerals.potassium = \
            str(data_zones["Zones"][str(key)]["kalium"]).strip()
        minerals.sodium = \
            str(data_zones["Zones"][str(key)]["natrium"]).strip()
        minerals.calcium = \
            str(data_zones["Zones"][str(key)]["calcium"]).strip()
        minerals.magnesium = \
            str(data_zones["Zones"][str(key)]["magnesium"]).strip()
        minerals.chloride = \
            str(data_zones["Zones"][str(key)]["chlorid"]).strip()
        minerals.nitrate = \
            str(data_zones["Zones"][str(key)]["nitrat"]).strip()
        minerals.sulfate = \
            str(data_zones["Zones"][str(key)]["sulfat"]).strip()
        minerals.save()

        if Measurement.objects.filter(location=location_exists):
            current_measurement = \
                create_current_measurement(data_zones, key, source,
                                           location_exists, minerals)
            current_measurement.save()
        else:
            location = Location()
            location.city = str(city).strip()
            location.district = str(suburb).strip()
            location.street = str(value).strip()
            location.zone = str(zone).strip()
            location.region = str(region).strip()
            location.save()

            current_measurement = \
                create_current_measurement(data_zones, key, source,
                                           location, minerals)
            current_measurement.save()

        return True
    except KeyError:
        if key not in NOT_INSERT:
            NOT_INSERT.append(key)
        return False


def create_current_measurement(data_zones, key, source, location, minerals):
    """
    Create current measurement.

    :param data_zones:
    :param key:
    :param source:
    :param location:
    :param minerals:
    """
    user = TapwaterUser.objects.get(pk=4)
    current_measurement = Measurement()
    current_measurement.date = \
        str(data_zones["Zones"][str(key)]["year"]).strip()
    current_measurement.source = str(source).strip()
    current_measurement.remarks = \
        str(data_zones["Zones"][str(key)]["description"]).strip()
    current_measurement.hardness = \
        str(data_zones["Zones"][str(key)]["hardness"]).strip()
    current_measurement.location = location
    current_measurement.minerals = minerals
    current_measurement.user = user

    return current_measurement


def flattens(json_dict_locations, parent_key='', sep='_'):
    """
    Iterate over the given JSON data and get all entries and objects.

    :param
        json_dict_locations (Dictionary): dictionary with all locations
        parent_key (String): parent key
        sep (String): seperator
    :return
        items: dictionary with items
    """
    items = []
    for key, value in json_dict_locations.items():
        new_key = parent_key + sep + key if parent_key else key
        if value and isinstance(value, collections.MutableMapping):
            items.extend(flattens(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def insert_user_to_database(row, contact_firstname, contact_lastname,
                            contact_mail, authority):
    """
    Try to write data (contact name, contact mail, municipalities) to posgres.

    :param
        row (String): the current row of contacts csv
        contact_name (String): Name of the contact person
        contact_mail (String): E-Mail of the contact person
        municipalities (String): municipalities of the contact person
    """
    try:
        user_type = TapwaterUserType.objects.get(value="AuthorityUser")
        current_user = TapwaterUser()
        current_user.firstname = str(contact_firstname).strip()
        current_user.lastname = str(contact_lastname).strip()
        current_user.email = str(contact_mail).strip()
        current_user.authority = str(authority).strip()
        current_user.type = user_type
        current_user.save()
        return True
    except KeyError:
        if row not in NOT_INSERT:
            NOT_INSERT.append(row)
        return False


def check_rollback(locations_file, zones_file, region):
    """
    Try to check if database rollback is needed.

    :param
        locations_file (Document): File with locations
        zones_file (Document): File with zones
        region (String): Measurment region
    """
    rollback = False
    for key, value in flattens(
            locations_file.load_location_json()).items():
        key = re.sub(' +', ' ', str(key))
        if len(value) > 0:
            for place in value:
                if not (insert_measurement_to_database(
                        key[10:], place, zones_file.load_zone_json(), region)):
                    rollback = True
        else:
            if not (insert_measurement_to_database(
                    key[10:], value, zones_file.load_zone_json(), region)):
                rollback = True
    return bool(rollback)


def user_not_exists(row, contact_firstname, contact_lastname,
                    contact_mail, authority):
    """
    Check if user not exists.

    :param
        row (String): Row with Name, E-Mail and municipalities
        contact_name (String): Name of the contact person
        contact_mail (String): E-Mail of the contact person
        municipalities (String): municipalities of the contact person
    """
    if TapwaterUser.objects.filter(firstname=contact_firstname,
                                   lastname=contact_lastname,
                                   email=contact_mail,
                                   authority=authority)\
            .exists():
        NOT_INSERT.append(row)
        return False
    return True


def generate_random_string(length):
    """Generate random string with digits."""
    random_string = string.ascii_letters + string.digits
    return ''.join(random.sample(random_string, length))


def send_admin_login_values(user, password):
    """
    Send login token for administrators.

    :param user:
    :param password:
    :return:
    """
    html_content = render_to_string('administration/email/'
                                    'administration_login.html',
                                    {'password': password,
                                     'user': user})
    text_content = strip_tags(html_content)
    email_subject = _(u'admin_manage_administrators_add_subject')
    email = EmailMultiAlternatives(email_subject, text_content,
                                   to=[user.email, ])
    email.attach_alternative(html_content, "text/html")
    try:
        return email.send()
    except socket.error:
        return False
