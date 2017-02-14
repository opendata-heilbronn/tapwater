
"""
Administration forms.

:copyright: (c) 2016 by Rohan Ahmed, Gregor Schäfer, Simon Scheuermann,
Florette Chamga, Benedikt Kurschatke
:license: MIT, see LICENSE
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from wasser.tapwater.models import AverageMeasurementValue, MineralWater


def validate_file_extension_json(value):
    """
    Validate the file extension for uploads.

    :param value:
    :return:
    """
    if not value.name.endswith('.json'):
        raise ValidationError(_(u'admin_forms_no_valid_json'))


def validate_file_extension_csv(value):
    """
    Validate the file extension for uploads.

    :param value:
    :return:
    """
    if not value.name.endswith('.csv'):
        raise ValidationError(_(u'admin_forms_value_csv'))


def validate_text_input(value):
    """
    Validate the input text.

    :param value:
    """
    if len(value) < 2 or len(value) > 100:
        raise ValidationError(_(u'admin_forms_value_region'))


class DocumentForm(forms.Form):
    """Form class for Document."""

    locations = forms.FileField(
        label=_(u'admin_forms_json_for_city'),
        widget=forms.FileInput(attrs={'class': 'btn btn-primary btn-file'}),
        validators=[validate_file_extension_json]
    )
    zones = forms.FileField(
        label=_(u'admin_forms_enter_json_for_zone'),
        widget=forms.FileInput(attrs={'class': 'btn btn-primary btn-file'}),
        validators=[validate_file_extension_json]
    )
    region = forms.CharField(
        label=_(u'admin_forms_location_of_region'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[validate_text_input]
    )


class ImportContactsDocumentForm(forms.Form):
    """Form class for ImportContactsDocument."""

    contacts = forms.FileField(
        label=_(u'admin_forms_csv_with_contacts'),
        widget=forms.FileInput(attrs={'class': 'btn btn-primary btn-file'}),
        validators=[validate_file_extension_csv]
    )


class AverageMeasurementForm(forms.ModelForm):
    """Form class for AverageMeasurementForm."""

    class Meta:
        """Meta Class for AverageMeasurementValue."""

        model = AverageMeasurementValue
        fields = [
            "sodium",
            "potassium",
            "calcium",
            "magnesium",
            "chloride",
            "nitrate",
            "sulfate",
            "hardness",
        ]

    sodium = forms.FloatField(
        label=_(u'admin_av_measure_value_natrium'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
        )

    potassium = forms.FloatField(
        label=_(u'admin_av_measure_value_potassium'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
        )

    calcium = forms.FloatField(
        label=_(u'admin_av_measure_value_calcium'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
        )

    magnesium = forms.FloatField(
        label=_(u'admin_av_measure_value_magnesium'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
        )

    chloride = forms.FloatField(
        label=_(u'admin_av_measure_value_chloride'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
        )

    nitrate = forms.FloatField(
        label=_(u'admin_av_measure_value_nitrate'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
        )

    sulfate = forms.FloatField(
        label=_(u'admin_av_measure_value_sulfate'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
        )

    hardness = forms.FloatField(
        label=_(u'admin_av_measure_value_hardness'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
        )


class MineralWaterForm(forms.ModelForm):
    """Form class for mineral waters."""

    class Meta:
        """Meta Class for mineral waters."""

        model = MineralWater
        fields = [
            "sodium",
            "potassium",
            "calcium",
            "magnesium",
            "chloride",
            "nitrate",
            "sulfate",
            "sources",
            "name",
            "key"
        ]

    name = forms.CharField(
        label=_(u'admin_mineral_water_name'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    key = forms.CharField(
        label=_(u'admin_mineral_water_key'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    sources = forms.CharField(
        label=_(u'admin_mineral_water_sources'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    sodium = forms.FloatField(
        label=_(u'admin_mineral_water_natrium'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
    )

    potassium = forms.FloatField(
        label=_(u'admin_mineral_water_potassium'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
    )

    calcium = forms.FloatField(
        label=_(u'admin_mineral_water_calcium'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
    )

    magnesium = forms.FloatField(
        label=_(u'admin_mineral_water_magnesium'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
    )

    chloride = forms.FloatField(
        label=_(u'admin_mineral_water_chloride'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
    )

    nitrate = forms.FloatField(
        label=_(u'admin_mineral_water_nitrate'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
    )

    sulfate = forms.FloatField(
        label=_(u'admin_mineral_water_sulfate'),
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'step': '0.01'}),
    )


class ManageAdministratorsForm(forms.Form):
    """Form class for mineral waters."""

    username = forms.CharField(
        label=_(u'admin_manage_administrators_username'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    first_name = forms.CharField(
        label=_(u'admin_manage_administrators_first_name'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    last_name = forms.CharField(
        label=_(u'admin_manage_administrators_last_name'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    email = forms.EmailField(
        label=_(u'admin_manage_administrators_email'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
