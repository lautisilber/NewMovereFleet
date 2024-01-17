from typing import Any, Dict, Mapping, Optional, Sequence, Type, Union
from django import forms
from django.core.files.base import File
from django.db import models
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.forms.widgets import Widget
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

from .models import Company, Vehicle, PartAbsProxy, PartWithLifespanAbs, PartTyreAbs, PartWithoutLifespanAbs, PartProxy, PartWithLifespan, PartTyre, PartWithoutLifespan

# class BaseForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(BaseForm, self).__init__(*args, **kwargs)
#         for bound_field in self:
#             if hasattr(bound_field, "field") and bound_field.field.required:
#                 bound_field.field.widget.attrs["required"] = "required"

# class BaseModelForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(BaseModelForm, self).__init__(*args, **kwargs)
#         for bound_field in self:
#             if hasattr(bound_field, "field") and bound_field.field.required:
#                 bound_field.field.widget.attrs["required"] = "required"

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


# class PartAbsBaseForm(forms.ModelForm):
#     content_type = forms.ModelChoiceField(required=True, empty_label=None, queryset=ContentType.objects.filter(model__in=(
#         PartWithLifespanAbs._meta.model_name,
#         PartTyreAbs._meta.model_name,
#         PartWithoutLifespanAbs._meta.model_name
#     )).all())

class PartWithLifespanAbsForm(forms.ModelForm):
    class Meta:
        model = PartWithLifespanAbs
        fields = '__all__'

class PartTyreAbsForm(forms.ModelForm):
    class Meta:
        model = PartTyreAbs
        fields = '__all__'

class PartWithoutLifespanAbsForm(forms.ModelForm):
    class Meta:
        model = PartWithoutLifespanAbs
        fields = '__all__'

class PartBaseForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(required=True, queryset=Vehicle.objects.all())
    def save(self, commit: bool=True):
        # can't really use this with commit = False
        instance = super(PartBaseForm, self).save(commit=False)

        instance._vehicle = self.cleaned_data['vehicle']
        print(instance._vehicle)

        if commit:
            self.save_m2m()
            instance.save()

        return instance

class PartWithLifespanForm(PartBaseForm):
    class Meta:
        model = PartWithLifespan
        fields = '__all__'
        # exclude = ('change_frequency_timedelta', 'change_frequency_km')

class PartTyreForm(PartBaseForm):
    class Meta:
        model = PartTyre
        fields = '__all__'
        # exclude = ('change_frequency_timedelta', 'change_frequency_km')

class PartWithoutLifespanForm(PartBaseForm):
    class Meta:
        model = PartWithoutLifespan
        fields = '__all__'