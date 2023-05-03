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
            self.fields[field].widget = self.fields[field].widget.__class__(attrs={'class': 'input'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    error_css_class = 'is-danger'
    required_css_class = 'is-warning'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = self.fields[field].widget.__class__(attrs={'class': 'input'})


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget = self.fields[field].widget.__class__(attrs={'class': 'input'})   

    class Meta:
        model = User
        fields = ['username', 'email']