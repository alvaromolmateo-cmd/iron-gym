from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from .models import MyUser


# UD5.2b - AuthenticationForm usa USERNAME_FIELD aunque el campo se llame username.
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={
        'class': 'form-control', 'autocomplete': 'username', 'autofocus': True,
    }))
    password = forms.CharField(label='Contraseña', strip=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'autocomplete': 'current-password',
    }))


# UD5.1 - Alta en el administrador sin guardar contraseñas en texto plano.
class MyUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'username')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirmation = cleaned_data.get('password2')
        if password and confirmation:
            if password != confirmation:
                self.add_error('password2', 'Las contraseñas no coinciden.')
            else:
                user = MyUser(email=cleaned_data.get('email', ''), username=cleaned_data.get('username'))
                validate_password(password, user)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# UD5.1 - El hash se muestra como información y no se edita como texto.
class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = '__all__'
