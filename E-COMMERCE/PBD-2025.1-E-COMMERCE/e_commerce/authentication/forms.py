from django import forms
from authentication.models import User


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ['username',
                  'password']


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email',
                  'first_name',
                  'last_name',
                  'phone',
                  'password']
