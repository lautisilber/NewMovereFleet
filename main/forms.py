from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from .models import QuestionInstance, QuestionTemplate, Company, Vehicle
from django.utils.translation import gettext_lazy
from datetime import datetime, timezone


def _bulma_text_input():
    return forms.widgets.TextInput(attrs={'class': 'input is-primary'})

def _bulma_number_input():
    return forms.widgets.NumberInput(attrs={'class': 'input is-primary'})

def _bulma_textarea(**attrs):
    attrs['class'] = 'input is-primary'
    return forms.widgets.Textarea(attrs=attrs)

def _bulma_checkbox(**attrs):
    attrs['class'] = 'is-checkradio'
    return forms.widgets.CheckboxInput(attrs=attrs)

class CompanyForm(forms.ModelForm):
    error_css_class = 'is-danger'
    required_css_class = 'is-warning'
    class Meta:
        model = Company
        fields = ['name']
        labels = {
            'name': 'Name'
        }
        widgets = {
            'name': _bulma_text_input()
        }

class VehicleForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = Vehicle
        fields = ['name', 'mileage', 'fuel', 'company']
        labels = {
            'name': 'Name',
            'mileage': 'Mileage',
            'fuel': 'Fuel',
            'company': 'Company'
        }
        widgets = {
            'name': _bulma_text_input(),
            'mileage': _bulma_number_input(),
            'fuel': _bulma_number_input(),
        }


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
        fields = ['question', 'info', 'allow_notes', 'vehicles', 'question_type', 'periodicity_days', 'periodicity_anchor', 'periodicity_days_notice', 'position_type']
        labels = {
            'question': 'Question',
            'info': 'Info',
            'allow_notes': 'Allow notes',
            'vehicles': 'Vehicles',
            'question_type': 'Question type',
            'periodicity_days': 'Periodicity days',
            'periodicity_anchor': 'Periodicity anchor',
            'periodicity_days_notice': 'Periodicity days notice',
            'position_type': 'Position type'
        }
        widgets = {
            'question': _bulma_text_input(),
            'info': _bulma_text_input(),
            'allow_notes': _bulma_checkbox(),
            'periodicity_days': _bulma_number_input(),
            'periodicity_anchor': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'periodicity_days_notice': _bulma_number_input()
        }


class QuestionAnswerForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'

    def __init__(self, *args, **kwargs):
        readonly_kwarg = 'readonly'
        readonly = readonly_kwarg in kwargs and kwargs[readonly_kwarg] is True
        if readonly_kwarg in kwargs:
            kwargs.pop(readonly_kwarg)
        super().__init__(*args, **kwargs)
        if readonly:
            for field in self.fields.values():
                field.disabled = True
        else:
            self.fields['answer_confirm'] = forms.BooleanField(help_text='Have you read the questions and answered conciously?', initial=False, required=True, widget=_bulma_checkbox(confirm_read='true'))

        allow_notes = self.instance.question_template.allow_notes if self.instance.question_template else True
        if not allow_notes:
            self.fields['notes'].widget = self.fields['notes'].hidden_widget()

    class Meta:
        model = QuestionInstance
        fields = ['answer', 'problem_description', 'notes']
        labels = {
            'answer': 'Answer',
            'problem_description': 'Problem description',
            'notes': 'Notes'
        }
        widgets = {
            'answer': _bulma_checkbox(),
            'problem_description': _bulma_textarea(rows=3),
            'notes': _bulma_textarea(rows=3)
        }