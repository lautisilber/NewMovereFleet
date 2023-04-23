from typing import Any, Dict, Optional, Type
from django import forms
from .models import QuestionInstance, QuestionTemplate, Company, Vehicle
from user.models import Profile
from django.utils.translation import gettext_lazy
from datetime import datetime, timezone


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


# class DateInputNow(forms.DateInput):
#     input_type = 'date'
#     def __init__(self, attrs = ..., format = ...) -> None:
#         super().__init__(attrs, format)

class QuestionForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'

    # def __init__(self, *args, **kwargs) -> None:
    #     super().__init__(*args, **kwargs)
    #     self.fields['periodicity_anchor'] = forms.DateField(initial=datetime.now(), widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = QuestionTemplate
        fields = '__all__' #['question', 'info', 'vehicles', 'periodicity_days', 'periodicity_days_notice', 'position_type']
        widgets = {
            'periodicity_anchor': forms.DateInput(attrs={'type': 'date'})
        }


class QuestionAnswerForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'

    class Meta:
        model = QuestionInstance
        fields = ['answer', 'notes']
