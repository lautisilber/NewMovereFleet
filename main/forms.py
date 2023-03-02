from django import forms
from .models import Checklist
from .models import ChecklistQuestion
from django.utils.translation import gettext_lazy


class ChecklistCreateForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = Checklist
        fields = ['template', 'name', 'vehicle']
        widgets = {'template': forms.HiddenInput()}

class ChecklistQuestionCreateForm(forms.ModelForm):
    error_css_class = 'form-error'
    required_css_class = 'form-required'
    class Meta:
        model = ChecklistQuestion
        fields = ['template', 'title', 'text', 'answer_type', 'allow_notes']
        widgets = {'template': forms.HiddenInput()}
        help_texts = {
            'answer_type': gettext_lazy('This includes general answer types and part-specific answer types')
        }
