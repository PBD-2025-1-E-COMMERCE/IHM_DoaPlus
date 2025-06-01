from django import forms
from app_ecommerce.models import Itens, Company


class CompanyLogin(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = ['cnpj', 'password']


class RegisterItem(forms.ModelForm):
    class Meta:
        model = Itens
        fields = ['code_item', 'name', 'category',
                  'description', 'stock_quantity', 'price', 'image']


class RegisterCompany(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'cnpj', 'logo', 'password', 'item', 'user']
