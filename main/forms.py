from typing import Any, Dict, Mapping, Optional, Sequence, Type, Union
from django import forms
from django.core.files.base import File
from django.db import models
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.forms.widgets import Widget
from .models import QuestionInstance, QuestionTemplate, Company, Vehicle, QuestionType
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError


def _bulma_text_input():
    return forms.widgets.TextInput(attrs={'class': 'input'})

def _bulma_number_input():
    return forms.widgets.NumberInput(attrs={'class': 'input'})

def _bulma_textarea(**attrs):
    attrs['class'] = 'input'
    return forms.widgets.Textarea(attrs=attrs)

def _bulma_checkbox(**attrs):
    return forms.widgets.CheckboxInput(attrs=attrs)

# class VehicleModelChoiceField(ModelChoiceField):
#     def __init__(self) -> None:
#         super().__init__(queryset=Vehicle.objects.all(), widget=_bulma_vehicle_modelchoicefield())
#     def label_from_instance(self, obj: Vehicle):
#         return obj.name

# def _bulma_vehicle_modelchoicefield():
#     return forms.widgets.SelectMultiple(attrs={'class': 'input'})

error_css_class = 'is-danger'

def form_init_add_errors(form: Union[forms.Form, forms.ModelForm]):
        for field in form.errors:
            if 'class' in form[field].field.widget.attrs:
                form[field].field.widget.attrs['class'] += ' ' + error_css_class
            else:
                form[field].field.widget.attrs['class'] += error_css_class

class ModelFormBulma(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        form_init_add_errors(self)

def form_set_checkboxes_initials(form: forms.ModelForm):
    if form.instance: # if there's a model instance
        for field_name, field in form.fields.items(): # for every field in the form
            if isinstance(field.widget, forms.widgets.CheckboxInput): # if the field's widget is a checkbox
                if hasattr(form.instance, field_name): # if the model has that field's name
                    if getattr(form.instance, field_name): # if the model's field is True
                        field.widget.attrs.update({'checked': 'true'})

class ModelFormWCheckbox(ModelFormBulma):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        form_set_checkboxes_initials(self)


class CompanyForm(ModelFormWCheckbox):
    class Meta:
        model = Company
        fields = ['name']
        labels = {
            'name': 'Nombre'
        }
        widgets = {
            'name': _bulma_text_input()
        }


class VehicleForm(ModelFormWCheckbox):
    class Meta:
        model = Vehicle
        fields = ['name', 'mileage', 'fuel', 'company']
        labels = {
            'name': 'Nombre',
            'mileage': 'Kilometraje',
            'fuel': 'Nafta',
            'company': 'Compañía'
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

class QuestionForm(ModelFormWCheckbox):
    class Meta:
        model = QuestionTemplate
        exclude = ['answer_sessions']
        labels = {
            'question': 'Pregunta',
            'info': 'Info',
            'allow_notes': 'Permitir notas',
            'vehicles': 'Vehículos',
            'periodicity_days': 'Periodicidad días',
            'periodicity_anchor': 'Periodicidad ancla',
            'periodicity_days_notice': 'Periodicidad días para responder',
            'position_type': 'Rol del usuario que responde'
        }
        widgets = {
            'question': _bulma_text_input(),
            'info': _bulma_text_input(),
            'allow_notes': _bulma_checkbox(),
            'periodicity_days': _bulma_number_input(),
            'periodicity_anchor': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'periodicity_days_notice': _bulma_number_input()
        }

class QuestionAnswerForm(ModelFormWCheckbox):
    def __init__(self, *args, **kwargs):
        readonly_kwarg = 'readonly'
        readonly = readonly_kwarg in kwargs and kwargs[readonly_kwarg] is True
        if readonly_kwarg in kwargs:
            kwargs.pop(readonly_kwarg)
        super().__init__(*args, **kwargs)
        # if not readonly:
        #     self.fields['answer_confirm'] = forms.BooleanField(help_text='Have you read the questions and answered conciously?', initial=False, required=True, widget=_bulma_checkbox())
        allow_notes = self.instance.question_template.allow_notes if self.instance.question_template else True
        if not allow_notes:
            self.fields['notes'].widget = self.fields['notes'].hidden_widget()
        
        if not readonly:
            # self.fields['answer'] = AnswerField()
            self.fields['answer'] = forms.BooleanField(widget=forms.widgets.RadioSelect(choices=[(True, 'Si'),  (False, 'No')]), label=gettext_lazy(QuestionAnswerForm.Meta.labels['answer']))

    class Meta:
        model = QuestionInstance
        fields = ['answer', 'problem_description', 'notes']
        labels = {
            'answer': 'Respuesta',
            'problem_description': 'Descripción del problema',
            'notes': 'Notas'
        }
        widgets = {
            'answer': _bulma_checkbox(),
            'problem_description': _bulma_textarea(rows=3),
            'notes': _bulma_textarea(rows=3)
        }


class QuestionTypeForm(ModelFormWCheckbox):
    class Meta:
        model = QuestionType
        fields = ['name', 'periodicity']
        labels = {
            'name': 'Nombre',
            'periodicity': 'Periodicidad'
        }
        widgets = {
            'name': _bulma_text_input(),
            'periodicity': _bulma_checkbox()
        }