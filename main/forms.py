from django import forms
from .models import Checklist
from .models import ChecklistQuestion


class ChecklistCreateForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['template', 'name', 'vehicle']
        widgets = {'template': forms.HiddenInput()}

class ChecklistQuestionCreateForm(forms.ModelForm):
    class Meta:
        model = ChecklistQuestion
        fields = ['template', 'title', 'text', 'answer_type', 'allow_notes']
        widgets = {'template': forms.HiddenInput()}