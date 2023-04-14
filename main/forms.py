from typing import Any, Dict, Optional, Type
from django import forms
from .models import ChecklistQuestionTemplate, Company, Vehicle
from user.models import Profile
from django.utils.translation import gettext_lazy


class CompanyForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = Company
        fields = ['name']

class VehicleForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = Vehicle
        fields = ['name', 'mileage', 'fuel', 'company']

class ChecklistQuestionForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = ChecklistQuestionTemplate
        fields = ['question', 'info', 'vehicles', 'periodicity_days', 'periodicity_days_notice', 'position_type']
        help_texts = {
            'answer_type': gettext_lazy('This includes general answer types and part-specific answer types')
        }
