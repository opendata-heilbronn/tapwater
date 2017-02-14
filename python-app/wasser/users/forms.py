
"""
Users forms.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from wasser.administration.models import TapwaterUser


class RegistrationFormPrivate(forms.Form):
    """Form class for private persons."""

    firstname = forms.RegexField(
        regex=r'[\w.@+-]+$',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_("users_registration_firstname"))

    lastname = forms.RegexField(
        regex=r'[\w.@+-]+$',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_("users_registration_lastname"))

    authority = forms.RegexField(
        regex=r'[\w.@+-]+$',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_("users_registration_authority"))

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=50,
        label=_("users_registration_email"))

    authority_checkbox = forms.BooleanField(
        required=False,
        label=_("users_registration_check_box"))

    def clean_email(self):
        """Failure if email is already in database."""
        email = self.cleaned_data['email']
        try:
            user = TapwaterUser.objects.get(email=email)
        except TapwaterUser.DoesNotExist:
            return email
        raise forms.ValidationError(
            _(u'email_already_in_db') + user.email)


class LoginForm(forms.Form):
    """Form class for login."""

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=50,
        label=_("users_registration_email"))

    def clean_email(self):
        """Failure if email not exists in database."""
        email = self.cleaned_data['email']
        try:
            user = TapwaterUser.objects.get(email=email)
        except TapwaterUser.DoesNotExist:
            raise forms.ValidationError(
                _(u'email_not_in_db'))
        else:
            return user.email
