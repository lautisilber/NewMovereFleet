from django import forms
from .models import ChecklistTemplate, ChecklistQuestionTemplate
from django.utils.translation import gettext_lazy


class ChecklistCreateForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = ChecklistTemplate
        fields = ['name', 'vehicle']

class ChecklistQuestionCreateForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = ChecklistQuestionTemplate
        fields = ['title', 'text', 'answer_type', 'allow_notes']
        help_texts = {
            'answer_type': gettext_lazy('This includes general answer types and part-specific answer types')
        }
