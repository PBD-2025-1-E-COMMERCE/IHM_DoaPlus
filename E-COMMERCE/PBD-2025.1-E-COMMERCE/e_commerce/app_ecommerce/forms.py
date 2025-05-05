from django import forms
from authentication.models import User


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Email')
    class Meta():
        model = User
        fields = ['username',
                  'password']
