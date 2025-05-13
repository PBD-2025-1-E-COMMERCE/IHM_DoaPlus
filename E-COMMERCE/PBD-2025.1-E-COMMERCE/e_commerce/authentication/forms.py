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
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite seu e-mail'
    }))
    first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite seu nome'
    }))
    last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite seu sobrenome'
    }))
    phone = forms.CharField(label='Telefone', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '(XX) XXXXX-XXXX'
    }))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite sua senha'
    }))

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'phone',
                  'password']
