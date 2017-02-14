"""
users views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from wasser.users.forms import RegistrationFormPrivate, LoginForm
from wasser.administration.models import TapwaterUser, TapwaterUserType
from wasser.login.utilities import send_login_token, send_registration_info, \
    user_logged_in
from wasser.users.models import (Measurement,
                                 Minerals,
                                 Location)


def insert_measurement(request):
    """
    Handle form post to insert measurement.

    :param request:
    :return: response
    """
    success = None
    if request.method == 'POST':
        success = True
        location_exists = Location()
        counter = 1
        while True:
            key = "street" + str(counter)
            if key in request.POST:
                if check_location_exists(request, counter):
                    location_exists = get_existing_location(request, counter)
                measurement_minerals = create_minerals(request)
                if not measurement_minerals.validate_model():
                    success = False
                    break
                hardness = request.POST["degree_of_hardness"]
                user = TapwaterUser.objects.get(pk=request.session['user'])

                if Measurement.objects.filter(location=location_exists):
                    current_measurement = \
                        create_current_measurement(request, location_exists,
                                                   user, measurement_minerals,
                                                   hardness)
                    if not current_measurement.add_measurement():
                        success = False
                    counter += 1
                else:
                    measurement_location = Location()
                    measurement_location.city = request.POST["city"]
                    measurement_location.region = request.POST["region"]
                    measurement_location.district = request.POST["district"]
                    street = request.POST["street" + str(counter)]
                    zone = request.POST["zone" + str(counter)]
                    measurement_location.street = street
                    measurement_location.zone = zone
                    if not measurement_location.validate_model():
                        success = False
                        break
                    current_measurement =\
                        create_current_measurement(request,
                                                   measurement_location,
                                                   user, measurement_minerals,
                                                   hardness)
                    if not current_measurement.add_measurement():
                        success = False
                    counter += 1
            else:
                break

    return render(request,
                  'users/insert_measurement.html',
                  {"success": success})


def check_location_exists(request, counter):
    """
    Check if location already exists.

    :param request:
    :param counter
    """
    return bool(Location.objects.filter(
        city=str(request.POST["city"]).strip(),
        district=str(request.POST["district"]).strip(),
        street=str(request.POST["street" + str(
            counter)]).strip(),
        zone=str(request.POST["zone" + str(counter)]).strip()).exists())


def get_existing_location(request, counter):
    """
    Get existing location.

    :param request:
    :param counter
    """
    return Location.objects.filter(
        city=str(request.POST["city"]).strip(),
        district=str(request.POST["district"]).strip(),
        street=str(request.POST["street" + str(
            counter)]).strip(),
        zone=str(request.POST["zone" + str(counter)]).strip()).first()


def create_current_measurement(request, location_exists, user,
                               measurement_minerals, hardness):
    """
    Create current measurement.

    :param request:
    :param location_exists:
    :param user:
    :param measurement_minerals:
    :param hardness:
    """
    current_measurement = Measurement()
    current_measurement.hardness = hardness
    current_measurement.date = request.POST["date"]
    current_measurement.source = request.POST["source"]
    current_measurement.remarks = request.POST["remarks"]
    current_measurement.minerals = measurement_minerals
    current_measurement.location = location_exists
    current_measurement.user = user

    return current_measurement


def create_minerals(request):
    """
    Create minerals.

    :param request:
    """
    measurement_minerals = Minerals()
    measurement_minerals.potassium = request.POST["potassium"]
    measurement_minerals.sodium = request.POST["sodium"]
    measurement_minerals.calcium = request.POST["calcium"]
    measurement_minerals.magnesium = request.POST["magnesium"]
    measurement_minerals.chloride = request.POST["chloride"]
    measurement_minerals.nitrate = request.POST["nitrate"]
    measurement_minerals.sulfate = request.POST["sulfate"]
    return (
        measurement_minerals)


def show_measurements_user(request):
    """
    Show all users which are stored into the database.

    :param request: Http request
    :return: render
    """
    user = TapwaterUser.objects.get(pk=request.session['user'])
    measurements = Measurement.objects.all().filter(user_id=user.id)
    return render(
        request,
        'users/show_measurements.html',
        {'measurements': measurements}
    )


def users_index(request):
    """Redirect to main site."""
    return render(request,
                  'users/index.html')


def registration(request):
    """
    Handle create private user form post.

    :param request:
    :return: response
    """
    if user_logged_in(request):
        return HttpResponseRedirect(reverse("users_index"))
    else:
        success = None
        if request.method == 'POST':
            form = RegistrationFormPrivate(request.POST)
            if form.is_valid():
                authority = str(form.cleaned_data['authority']).strip()

                if authority:
                    user_type = TapwaterUserType.objects.get(
                        value="AuthorityUser")
                else:
                    user_type = TapwaterUserType.objects.get(
                        value="PrivateUser")

                current_user = TapwaterUser()
                current_user.firstname = str(form.cleaned_data['firstname'])\
                    .strip()
                current_user.lastname = \
                    str(form.cleaned_data['lastname']).strip()
                current_user.authority = authority
                current_user.email = str(form.cleaned_data['email']).strip()
                current_user.type = user_type
                current_user.save()
                send_registration_info(current_user)
                success = True
                form = RegistrationFormPrivate()
            else:
                success = False
        else:
            form = RegistrationFormPrivate()

    return render(request, 'users/registration.html',
                  {'form': form, "success": success})


def users_logout(request):
    """
    Kill Session for Office Logout.

    :param request:
    :return:
    """
    request.session.set_expiry(-100)
    request.session.clear_expired()
    messages.add_message(request, messages.SUCCESS,
                         _('login_index_logout_msg'), extra_tags='logout_msg')

    return HttpResponseRedirect(reverse("index"))


def send_token_for_one_user(request):
    """
    Send token for one user.

    :param request:Http request
    :return:render
    """
    data = dict()

    if request.method == 'POST':
        user_mail = request.POST.get('email')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = TapwaterUser.objects.get(email=user_mail)
            if send_login_token(user, request):
                data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = LoginForm()

    context = {'form': form}
    data['html_form'] = render_to_string(
        'tapwater/modals/modal_login.html',
        context,
        request=request
        )
    return JsonResponse(data)
