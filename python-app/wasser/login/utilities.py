"""
Login utilities for token handling.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

import uuid
import socket
from functools import wraps
from datetime import datetime, timedelta

from django.shortcuts import render, reverse, get_object_or_404
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from wasser.administration.models import (Token)
from wasser.settings import SESSION_EXPIRES_SECONDS


def login_required(view_func):
    """
    Wrapper function for checking the session.

    :param
    """
    def _login_required(request, *args, **kwargs):
        # action before view_func call
        if "user" not in request.session:
            return render(request, 'login/login_failed.html')

        user_id = request.session["user"]
        user_token = request.session["token"]

        current_token = get_object_or_404(Token, value=user_token,
                                          user_id=user_id)

        if token_valid(current_token):
            # update session expire
            update_user_session(request)
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return render(request, 'login/login_failed.html', )

    return wraps(view_func)(_login_required)


def admin_login_required(view_func):
    """
    Wrapper function for checking the admin session.

    :param

    """
    def _admin_login_required(request, *args, **kwargs):
        if request.user.is_authenticated:
            response = view_func(request, *args, **kwargs)
        else:
            return render(request, 'login/admin_login_failed.html')
        # do action after view_func call
        return response
    return wraps(view_func)(_admin_login_required)


def user_logged_in(request):
    """
    Test if the user is logged in as user.

    :param
    """
    if "user" not in request.session:
        return False
    else:
        user_id = request.session["user"]
        user_token = request.session["token"]

        current_token = get_object_or_404(Token, value=user_token,
                                          user_id=user_id)

        return bool(token_valid(current_token))


def token_valid(token):
    """
    Validate Token.

    :param
    token_db(String): String of valid Date of Token
    """
    # get session by key
    # save new valid until
    date = datetime.now().date()
    if token.valid_until >= date:
        return bool(True)
    else:
        return False


def create_user_session(request, username, token):
    """Create the user session."""
    request.session.set_expiry(SESSION_EXPIRES_SECONDS)
    request.session["user"] = username
    request.session["token"] = token


def update_user_session(request):
    """
    Update User session.

    :param
    """
    request.session.set_expiry(SESSION_EXPIRES_SECONDS)


def send_login_token(user, request):
    """
    Send a login token to a user.

    :param user:
    :param request:
    :return:
    """
    server_address = ""
    if "HTTP_HOST" in request.META:
        server_address = request.META['HTTP_HOST']

    # Create a random token with UUID
    uuid.uuid4()
    token = (str(uuid.uuid4())).replace("-", "")
    generated_token = (server_address + reverse("login_authority")
                       + "?id=" + str(user.id) + '&token=' + token)
    html_content = render_to_string('login/email/token.html',
                                    {'token': generated_token,
                                     'user': user})
    text_content = strip_tags(html_content)
    email_subject = _(u'login_email_token_subject')
    email = EmailMultiAlternatives(email_subject, text_content,
                                   to=[user.email, ])
    email.attach_alternative(html_content, "text/html")
    try:
        validate_email(user.email)
    except ValidationError:
        return False
    else:
        if save_token(user.id, token):
            try:
                return email.send()
            except socket.error:
                return False
    return False


def send_registration_info(user):
    """
    Send a registration info to new users.

    :param user:
    :return:
    """
    html_content = render_to_string('users/email/registration.html',
                                    {'user': user, })
    text_content = strip_tags(html_content)
    email_subject = _(u'login_utilities_registration_subject')
    email = EmailMultiAlternatives(email_subject, text_content,
                                   to=[user.email, ])
    email.attach_alternative(html_content, "text/html")
    try:
        validate_email(user.email)
    except ValidationError:
        return False
    else:
        try:
            return email.send()
        except socket.error:
            return False


def save_token(id_user, token):
    """
    Save Token in DB.

    :param
    valid_until (date): Date for token validation
    token (String): Token for User Login
    id_user(String): User Id
    """
    date = datetime.now() + timedelta(days=14)
    valid_until = date.strftime("%Y-%m-%d")

    security_token = Token()
    security_token.value = token
    security_token.valid_until = valid_until
    security_token.user_id = id_user
    security_token.save()
    return security_token.id
