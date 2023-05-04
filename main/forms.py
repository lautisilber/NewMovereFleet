from typing import Any, Callable, Dict, Optional, Union
from django import forms
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from .models import QuestionInstance, QuestionTemplate, Company, Vehicle
from django.utils.translation import gettext_lazy
from django.forms import ModelChoiceField


def _bulma_text_input():
    return forms.widgets.TextInput(attrs={'class': 'input'})

def _bulma_number_input():
    return forms.widgets.NumberInput(attrs={'class': 'input'})

def _bulma_textarea(**attrs):
    attrs['class'] = 'input'
    return forms.widgets.Textarea(attrs=attrs)

def _bulma_checkbox(**attrs):
    return forms.widgets.CheckboxInput(attrs=attrs)

class VehicleModelChoiceField(ModelChoiceField):
    def __init__(self) -> None:
        super().__init__(queryset=Vehicle.objects.all(), widget=_bulma_vehicle_modelchoicefield())
    def label_from_instance(self, obj: Vehicle):
        return obj.name

def _bulma_vehicle_modelchoicefield():
    return forms.widgets.SelectMultiple(attrs={'class': 'input'})

error_css_class = 'is-danger'

def form_init_add_errors(form: Union[forms.Form, forms.ModelForm]):
        for field in form.errors:
            if 'class' in form[field].field.widget.attrs:
                form[field].field.widget.attrs['class'] += ' ' + error_css_class
            else:
                form[field].field.widget.attrs['class'] += error_css_class

class CompanyForm(forms.ModelForm):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        form_init_add_errors(self)

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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        form_init_add_errors(self)

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
    vehicles = VehicleModelChoiceField()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        form_init_add_errors(self)

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

    def __init__(self, *args, **kwargs):
        readonly_kwarg = 'readonly'
        readonly = readonly_kwarg in kwargs and kwargs[readonly_kwarg] is True
        if readonly_kwarg in kwargs:
            kwargs.pop(readonly_kwarg)
        super().__init__(*args, **kwargs)
        if readonly:
            for field in self.fields.values():
                field.readonly = True
        else:
            self.fields['answer_confirm'] = forms.BooleanField(help_text='Have you read the questions and answered conciously?', initial=False, required=True, widget=_bulma_checkbox())

        allow_notes = self.instance.question_template.allow_notes if self.instance.question_template else True
        if not allow_notes:
            self.fields['notes'].widget = self.fields['notes'].hidden_widget()
        
        form_init_add_errors(self)

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