from django import forms
from app_ecommerce.models import Item, Company


class CompanyLogin(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = ['cnpj', 'password']


class RegisterItem(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code_item', 'name', 'category',
                  'level', 'company_id', 'image']


class RegisterCompany(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'cnpj', 'logo', 'categorys']
