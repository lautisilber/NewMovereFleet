from typing import Any, Dict, Mapping, Optional, Sequence, Type, Union
from django import forms
from django.core.files.base import File
from django.db import models
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.forms.widgets import Widget
from .models import Company, Vehicle
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError

exclude_timestamp_mixin = ('created_at', 'updated_at')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = exclude_timestamp_mixin

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = exclude_timestamp_mixin