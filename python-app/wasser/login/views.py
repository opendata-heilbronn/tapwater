"""
login views.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from wasser.login.utilities import (token_valid, create_user_session)
from wasser.administration.models import Token


def login_authority(request):
    """
    Show login for an office.

    :param request:
    :return:
    """
    token = request.GET.get('token')
    user_id = request.GET.get('id')

    if token and user_id:
        current_token = get_object_or_404(Token, value=token, user_id=user_id)

        validation = token_valid(current_token)

        if validation is True:
            create_user_session(request, username=user_id, token=token)
            return redirect(reverse("users_index"))
        else:
            messages.add_message(request, messages.WARNING,
                                 _('index_login_invalid_token'))

    return redirect(reverse("index"))


def login_failed(request):
    """
    Show login failed.

    :param request:
    :return:
    """
    return render(request, 'login/login_failed.html', {})


def login_admin(request):
    """
    Show login for a private person.

    :param request:
    :return:
    """
    error_msg = ""
    if request.method == "POST":
        user = authenticate(username=request.POST["user"],
                            password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect(reverse("admin_index"))
        else:
            error_msg = str(_(u'admin_login_failed_error_msg'))
    return render(request, "login/admin.html", {"error_msg": error_msg})


def admin_login_failed(request):
    """
    Show admin login failed.

    :param request:
    :return:
    """
    return render(request, 'login/admin_login_failed.html', {})
