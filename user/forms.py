from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    error_css_class = 'is-danger'
    required_css_class = 'is-warning'
    email = forms.EmailField(label='Email')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'class' in self[field].field.widget.attrs:
                self[field].field.widget.attrs['class'] += ' input'
            else:
                self[field].field.widget.attrs['class'] = 'input'
        for field in self.errors:
            self[field].field.widget.attrs['class'] += ' ' + UserRegisterForm.error_css_class

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    error_css_class = 'is-danger'
    required_css_class = 'is-warning'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        all_errors = list(self.errors) == ['__all__']
        print(list(self.errors))
        for field in self.fields:
            if field == '__all__': continue
            if 'class' in self[field].field.widget.attrs:
                self[field].field.widget.attrs['class'] += ' input'
            else:
                self[field].field.widget.attrs['class'] = 'input'
            if all_errors:
                self[field].field.widget.attrs['class'] += ' ' + UserLoginForm.error_css_class
        for field in self.errors:
            if field == '__all__': continue
            self[field].field.widget.attrs['class'] += ' ' + UserLoginForm.error_css_class


class UserUpdateForm(forms.ModelForm):
    error_css_class = 'is-danger'
    required_css_class = 'is-warning'

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Username',
            'email': 'Email'
        }
        widgets = {
            'username': forms.widgets.TextInput(attrs={'class': 'input'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'input'})
        }