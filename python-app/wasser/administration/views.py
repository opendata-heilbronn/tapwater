"""
Administration views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from wasser.administration.forms import (DocumentForm,
                                         ImportContactsDocumentForm,
                                         AverageMeasurementForm,
                                         MineralWaterForm,
                                         ManageAdministratorsForm)
from wasser.administration.models import (ImportMeasurementsDocument,
                                          ImportContactsDocument,
                                          TapwaterUser,
                                          Token)
from wasser.administration.utilities import (insert_user_to_database,
                                             check_rollback, NOT_INSERT,
                                             user_not_exists,
                                             generate_random_string,
                                             send_admin_login_values)
from wasser.login.utilities import send_login_token
from wasser.tapwater.models import (AverageMeasurementValue, MineralWater,
                                    NutrientDailyDosis)
from wasser.users.models import Measurement, Location


def show_measurements(request):
    """
    Show all measurements which are stored into the database.

    :param request: Http request
    :return: render
    """
    page = request.GET.get('page', 1)

    measurements_l = Measurement.objects.all().order_by("date")
    paginator = Paginator(measurements_l, 50)
    try:
        measurements = paginator.page(page)
    except PageNotAnInteger:
        measurements = paginator.page(1)
    except EmptyPage:
        measurements = paginator.page(paginator.num_pages)

    index = measurements.number - 1

    max_index = len(paginator.page_range)

    # We want a range of 7, so we calculate where to slice the list.
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index

    # New page range.
    page_range = paginator.page_range[start_index:end_index]

    return render(
        request,
        'administration/measurements.html',
        {'measurements': measurements, 'page_range': page_range}
    )


def show_locations(request):
    """
    Show all mineral waters.

    :param request:
    :return:
    """
    page = request.GET.get('page', 1)
    locations_l = Location.objects.all().order_by('city')
    paginator = Paginator(locations_l, 50)
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)

    index = locations.number - 1

    max_index = len(paginator.page_range)

    # We want a range of 7, so we calculate where to slice the list.
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index

    # New page range.
    page_range = paginator.page_range[start_index:end_index]
    return render(
        request,
        'administration/locations.html',
        {'locations': locations, 'page_range': page_range}
    )


def show_mineral_waters(request):
    """
    Show all mineral waters.

    :param request:
    :return:
    """
    mineral_waters = MineralWater.objects.order_by('name')
    return render(
        request,
        'administration/mineral_waters.html',
        {'mineral_waters': mineral_waters}
    )


def show_average_measurement_value(request):
    """
    Show average measurement values.

    :param request:
    :return:
    """
    queryset = AverageMeasurementValue.objects.all()
    context = {
        "average_measurement_values": queryset
    }

    return render(
        request,
        'administration/average_measurement_value.html',
        context
    )


def edit_average_measurement_value(request, primary=1):
    """
    Update average measurement.

    :param request:
    :param primary:
    :return:
    """
    success = None
    instance = get_object_or_404(AverageMeasurementValue, pk=primary)
    form = AverageMeasurementForm(request.POST or None, instance=instance)
    if request.method == "POST":

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, messages)
            success = True
        else:
            success = False

    return render(request,
                  'administration/edit_average_measurement_value.html',
                  {'instance': instance,
                   'form': form,
                   'success': success})


def show_nutrient_daily_dosis(request):
    """
    Show nutrient daily dosis.

    :param request:
    :return:
    """
    nutrient_daily_dosis = NutrientDailyDosis.objects.get(pk=1)
    return render(
        request,
        'administration/nutrient_daily_dosis.html',
        {'nutrient_daily_dosis': nutrient_daily_dosis}
    )


@transaction.atomic
def import_measurements(request):
    """
    Import values from JSON-Files.

    :param request: Http request
    :return: render
    """
    not_insert = []
    success = None

    sid = transaction.savepoint()
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            locations_file = \
                ImportMeasurementsDocument(
                    locations=request.FILES['locations'])
            locations_file.save()
            zones_file = ImportMeasurementsDocument(
                zones=request.FILES['zones'])
            zones_file.save()
            region = form.cleaned_data['region']
            del NOT_INSERT[:]
            if(zones_file.is_valid_json_zone()
               and locations_file.is_valid_json_location() and region):
                try:
                    with transaction.atomic():
                        rollback = check_rollback(locations_file, zones_file,
                                                  region)
                    if rollback:
                        success = False
                        not_insert = NOT_INSERT
                        transaction.savepoint_rollback(sid)
                    else:
                        success = True
                except ValueError:
                    success = False
                    transaction.savepoint_rollback(sid)

            else:
                success = False
        else:
            success = False
    else:
        form = DocumentForm()

    # Render page with the form
    return render(
        request,
        'administration/import_measurements.html',
        {'form': form, 'success': success, 'not_insert': not_insert}
    )


@transaction.atomic
def import_contacts(request):
    """
    Import values from CSV-Files.

    :param request: Http request
    :return: render
    """
    not_insert = []
    success = None

    sid = transaction.savepoint()
    # Handle file upload
    if request.method == 'POST':
        form = ImportContactsDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            contacts_file = \
                ImportContactsDocument(contacts=request.FILES['contacts'])
            contacts_file.save()
            rollback = False
            del NOT_INSERT[:]
            if contacts_file.is_valid_csv():
                try:
                    with transaction.atomic():
                        for row in contacts_file.load_contacts_csv():
                            if user_not_exists(row, row[0], row[1], row[2],
                                               row[3]):

                                insert_user_to_database(str(row), row[0],
                                                        row[1], row[2],
                                                        row[3])
                            else:
                                rollback = True
                    if rollback:
                        success = False
                        not_insert = NOT_INSERT
                        transaction.savepoint_rollback(sid)
                    else:
                        success = True
                except ValueError:
                    success = False
                    transaction.savepoint_rollback(sid)

            else:
                success = False
        else:
            success = False
    else:
        form = ImportContactsDocumentForm()

    return render(
        request,
        'administration/administrate_authority.html',
        {'form': form, 'success': success, 'not_insert': not_insert}
    )


def show_users(request):
    """
    Show all users which are stored into the database.

    :param request: Http request
    :return: render
    """
    page = request.GET.get('page', 1)

    users_l = TapwaterUser.objects.order_by('lastname')

    paginator = Paginator(users_l, 50)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    index = users.number - 1

    max_index = len(paginator.page_range)

    # We want a range of 7, so we calculate where to slice the list.
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index

    # New page range.
    page_range = paginator.page_range[start_index:end_index]

    return render(
        request,
        'administration/show_users.html',
        {'users': users, 'page_range': page_range}
    )


def admin_index(request):
    """Show to main site."""
    return render(
        request,
        'administration/index.html'
    )


def send_token_for_all_users(request):
    """
    Send a token to all users.

    :param request:Http request
    :return:render
    """
    send_success = bool(False)
    users = TapwaterUser.objects.filter(type__value="AuthorityUser")
    for user in users:
        if send_login_token(user, request):
            send_success = bool(True)

    form = ImportContactsDocumentForm()

    return render(
        request,
        'administration/administrate_authority.html',
        {'form': form, 'send_success': send_success}
    )


def send_token_for_selected_user(request):
    """
    Send a token for select users.

    :param request:
    :return:
    """
    # declare vars
    success = None
    failed_users = []
    form_users = []
    checked_users_len = None

    # load all users and load all active tokens to each users
    all_users = TapwaterUser.objects.filter(type__value="AuthorityUser") \
        .order_by('firstname')
    for user in all_users:
        valid_token = Token.objects.filter(user_id=user.id, )
        form_users.append({"firstname": user.firstname,
                           "lastname": user.lastname,
                           "email": user.email,
                           "valid_token": len(valid_token),
                           "id": user.id})

    # send mails to each selected user on post
    if request.method == "POST":
        checked_users = request.POST.getlist('sendToken[]')
        checked_users_len = len(checked_users)
        if checked_users_len:
            success = True
            for user_id in checked_users:
                try:
                    current_user = TapwaterUser.objects.get(pk=user_id)
                    if not send_login_token(current_user, request):
                        success = False
                        failed_users.append(current_user.lastname)
                except ObjectDoesNotExist:
                    success = False
                    failed_users.append(
                        _(u'administration_token_no_valid_user')
                    )

    return render(
        request,
        'administration/send_token.html',
        {"users": form_users,
         "success": success,
         "failed_users": failed_users,
         "checked_users_len": checked_users_len}
    )


def confirm_authority_user(request):
    """
    Verify selected users.

    :param request:
    :return:
    """
    # declare vars
    success = None
    failed_users = []
    form_users = []
    checked_users_len = None

    # load all unverified authority users
    all_unverified_authority_user = TapwaterUser.objects.filter(
        type__value="AuthorityUser", verified=False).order_by('firstname')
    for user in all_unverified_authority_user:
        valid_token = Token.objects.filter(user_id=user.id, )
        form_users.append({"firstname": user.firstname,
                           "lastname": user.lastname,
                           "email": user.email,
                           "valid_token": len(valid_token),
                           "id": user.id,
                           "authority": user.authority})

    if request.method == "POST":
        checked_users = request.POST.getlist('verifyUsers[]')
        checked_users_len = len(checked_users)
        if checked_users_len:
            success = True
            for user_id in checked_users:
                try:
                    current_user = TapwaterUser.objects.get(pk=user_id)
                    current_user.verified = True
                    current_user.save()
                except ObjectDoesNotExist:
                    success = False
                    failed_users.append(
                        _(u'administration_verifikation_no_valid_user')
                    )

    return render(
        request,
        'administration/confirm_users.html',
        {"users": form_users,
         "success": success,
         "failed_users": failed_users,
         "checked_users_len": checked_users_len}
    )


def delete_user(request, user_id):
    """Delete user site."""
    if request:
        user = get_object_or_404(TapwaterUser, pk=user_id)
        TapwaterUser.delete(user)
        return HttpResponseRedirect(reverse("show_users"))


def show_history(request, location_id):
    """
    Show measurements for a specific location.

    :param request:
    :param location_id:
    :return:
    """
    measurement = Measurement.objects.all().filter(location_id=location_id)
    return render(
        request,
        'administration/show_history.html',
        {"measurement": measurement}
    )


def edit_mineral_water(request, mineral_water_id):
    """
    Edit single mineral water.

    :param request:
    :param mineral_water_id: ID of the current mineral water
    :return:
    """
    success = None
    mineral_water = get_object_or_404(MineralWater, pk=mineral_water_id)
    form = MineralWaterForm(request.POST or None, instance=mineral_water)
    if request.method == "POST":
        success = False
        # check form is valid
        if form.is_valid():
            # check key or name of water already exists
            key_exists = MineralWater.objects.filter(
                key=request.POST['key']).exclude(id=mineral_water.id)
            name_exists = MineralWater.objects.filter(
                name=request.POST['name']).exclude(id=mineral_water.id)
            if len(key_exists) == 0 and len(name_exists) == 0:
                mineral_water = form.save(commit=False)
                mineral_water.save()
                success = True

    return render(
        request,
        'administration/edit_mineral_water.html',
        {'mineral_water': mineral_water,
         'form': form,
         'success': success})


def add_mineral_water(request):
    """
    Add a mineral water.

    :param request:
    :return:
    """
    success = None
    form = MineralWaterForm(request.POST)
    if request.method == "POST":
        success = False
        # check form is valid
        if form.is_valid():
            # check key or name of water already exists
            key_exists = MineralWater.objects.filter(
                key=request.POST['key'])
            name_exists = MineralWater.objects.filter(
                name=request.POST['name'])
            if len(key_exists) == 0 and len(name_exists) == 0:
                mineral_water = form.save(commit=False)
                mineral_water.referenced = False
                mineral_water.save()
                success = True

    return render(
        request,
        'administration/add_mineral_water.html',
        {'form': form, 'success': success})


def delete_mineral_water(request, mineral_water_id):
    """Delete a single mineral water."""
    if request:
        mineral_water = get_object_or_404(MineralWater, pk=mineral_water_id)
        MineralWater.delete(mineral_water)
        url_to_return = reverse('show_mineral_waters')
        messages.add_message(request, messages.SUCCESS,
                             _('administration_delete_water_msg'),
                             extra_tags='delete_msg')
        return HttpResponseRedirect(url_to_return)


def admin_logout(request):
    """
    Logout admins.

    :param request:
    :return:
    """
    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         _('login_index_logout_msg'), extra_tags='logout_msg')

    return HttpResponseRedirect(reverse("index"))


def manage_users(request):
    """
    Manage users page.

    :param request:
    :return:
    """
    not_insert = []
    success = None
    form = ImportContactsDocumentForm()
    return render(
        request,
        'administration/administrate_authority.html',
        {'form': form, 'success': success, 'not_insert': not_insert}
    )


def manage_administrators(request):
    """
    Main Page to manage administrators.

    :param request:
    :return:
    """
    success = None
    all_users = User.objects.all()
    form = ManageAdministratorsForm()

    return render(
        request,
        'administration/administrate_administrators.html',
        {'form': form,
         "all_users": all_users,
         "success": success})


def add_admin(request):
    """
    Route to add administrators.

    :param request:
    :return:
    """
    success = None
    all_users = User.objects.all()
    form = ManageAdministratorsForm(request.POST)
    if request.method == "POST":
        success = False
        # check form
        if form.is_valid():
            # check username already exists
            current_user = User.objects.filter(
                username=request.POST["username"])
            if not current_user:
                # create user
                password = generate_random_string(8)
                new_user = User()
                new_user.username = request.POST["username"]
                new_user.first_name = request.POST["first_name"]
                new_user.last_name = request.POST["last_name"]
                new_user.email = request.POST["email"]
                new_user.set_password(password)
                new_user.save()
                # send email
                if send_admin_login_values(new_user, password):
                    success = True
                    form = ManageAdministratorsForm()  # clear form
    return render(
        request,
        'administration/administrate_administrators.html',
        {'form': form,
         "all_users": all_users,
         "success": success})


def delete_admin(request, user_id):
    """
    Delete an admin.

    :param request:
    :param user_id: The user id of the current admin
    :return: reverse to manage page
    """
    current_user = get_object_or_404(User, id=user_id)
    current_user.delete()
    messages.add_message(request, messages.SUCCESS,
                         _('admin_manage_administrators_delete_successful'))

    return HttpResponseRedirect(reverse("manage_administrators"))


def change_password(request):
    """
    Change current password.

    :param request:
    :return:
    """
    if request.method == "POST":
        new_password = request.POST["new_password"].strip()
        new_password_repeat = request.POST["new_password_repeat"].strip()
        if new_password != "" and new_password_repeat != "":
            if new_password == new_password_repeat:
                current_user = get_object_or_404(User, id=request.user.id)
                current_user.set_password(new_password)
                current_user.save()
                messages.add_message(request, messages.SUCCESS,
                                     _('admin_change_password_successful'))
                user = authenticate(username=request.user,
                                    password=new_password)
                if user is not None:
                    login(request, user)
            else:
                messages.add_message(request, messages.ERROR,
                                     _('admin_change_password_'
                                       'error_different'))
        else:
            messages.add_message(request, messages.ERROR,
                                 _('admin_change_password_error_empty'))

        return HttpResponseRedirect(reverse("change_admin_password"))

    return render(
        request,
        'administration/change_password.html', {})
