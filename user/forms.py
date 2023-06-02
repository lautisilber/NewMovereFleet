from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, UsernameField
from django.utils.translation import gettext_lazy
from django.utils.html import format_html

from .models import Profile


class UserRegisterForm(UserCreationForm):
    error_css_class = 'is-danger'
    required_css_class = 'is-warning'
    email = forms.EmailField(label='Email', required=False)
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new_password'}),
        help_text=format_html(gettext_lazy('Su contraseña no puede ser demasiado similar a su otra información personal.</br>Su contraseña debe contener al menos 8 caracteres.</br>Su contraseña no puede ser una contraseña de uso común.</br>Su contraseña no puede ser completamente numérica.'))
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new_password'})
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        profile = False
        if 'profile' in kwargs:
            profile = kwargs['profile']
            kwargs.pop('profile')
        super().__init__(*args, **kwargs)
        if profile:
                self.fields['position_type'] = forms.ChoiceField(choices=Profile.PositionType.choices)
        for field in self.fields:
            if 'class' in self[field].field.widget.attrs:
                self[field].field.widget.attrs['class'] += ' input'
            else:
                self[field].field.widget.attrs['class'] = 'input'
        for field in self.errors:
            self[field].field.widget.attrs['class'] += ' ' + UserRegisterForm.error_css_class
        self.fields['password1'].label = 'CACA'

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
        }
    
    def save(self):
        instance = super().save(commit=True)
        if 'position_type' in self.fields:
            print(self.cleaned_data['position_type'])
            instance.profile.position_type = self.cleaned_data['position_type']
            instance.profile.save()
        instance.save()
        return instance



class UserLoginForm(AuthenticationForm):
    error_css_class = 'is-danger'
    required_css_class = 'is-warning'

    username = UsernameField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'autofocus': True, 'autocapitalize': 'none', 'autocomplete': 'username', 'maxlength': 150})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current_password'})
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        all_errors = list(self.errors) == ['__all__']
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
        # for l_k, l_v in {'username': 'Nombre de usuario', 'password': 'Contraseña'}.items():
        #     if l_k in self.fields:
        #         self.fields[l_k].label = l_v
        #         print(l_k, l_v, self.fields[l_k].label)


from main.forms import form_init_add_errors

class UserAdminUpdateForm(forms.ModelForm):
    error_css_class = 'is-danger'
    required_css_class = 'is-warning'

    position_type = forms.ChoiceField(choices=Profile.PositionType.choices, widget=forms.widgets.Select(attrs={'class': 'input'}))

    def __init__(self, *args, **kwargs):
        if 'instance' not in kwargs:
            raise Exception
        if 'initial' in kwargs and isinstance(kwargs['initial'], dict):
            kwargs['initial']['password'] = ''
        else:
            kwargs['initial'] = {'password': ''}
        kwargs['initial']['position_type'] = kwargs['instance'].profile.position_type
        super().__init__(*args, **kwargs)
        form_init_add_errors(self)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Email',
            'password': 'Contraseña'
        }
        widgets = {
            'username': forms.widgets.TextInput(attrs={'class': 'input'}),
            'email': forms.widgets.EmailInput(attrs={'class': 'input'}),
            'password': forms.widgets.TextInput(attrs={'class': 'input'})
        }
    
    def save(self):
        instance = super().save(commit=False)
        if 'password' in self.cleaned_data:
            instance.set_password(self.cleaned_data['password'])
        instance.save()
        if 'position_type' in self.cleaned_data:
            instance.profile.position_type = self.cleaned_data['position_type']
            instance.profile.save()
        return instance
