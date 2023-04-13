from django import forms
from .models import ChecklistTemplate, ChecklistQuestionTemplate, Company, Vehicle
from django.utils.translation import gettext_lazy


class CompanyForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = Company
        fields = ['name']

class VehicleForm(form.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = Vehicle
        fields = ['name', 'mileage', 'fuel', 'vehicle_type', 'drivetrain_type', 'company']

class ChecklistForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = ChecklistTemplate
        fields = ['name', 'vehicle']

class ChecklistQuestionForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = ChecklistQuestionTemplate
        fields = ['title', 'text', 'answer_type', 'allow_notes']
        help_texts = {
            'answer_type': gettext_lazy('This includes general answer types and part-specific answer types')
        }
