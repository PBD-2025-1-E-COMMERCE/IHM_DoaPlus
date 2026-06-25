from django import forms
from django.contrib import admin
from .models import _Group, Group, User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False, widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        required=False, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = "__all__"

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password and new_password != confirm_password:
            raise ValidationError({"new_password": "Passwords must be equal"})
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserForm

    def get_fieldsets(self, request, obj=...):
        fieldsets = [
            ("User Info", {"fields": [
             "email", "first_name", "last_name", "phone", "company", "cupom"]}),
        ]
        if obj:
            fieldsets += [
                ("Simple permissions", {"fields": [
                 "is_staff", "is_active", "is_superuser", "is_admin"]}),
                ("Advanced permissions", {
                 "fields": ["user_permissions", "groups"]}),
            ]
        else:
            fieldsets.append(
                ("Security", {"fields": ["new_password", "confirm_password"]})
            )
        return fieldsets


admin.site.unregister(_Group)
admin.site.register(Group)

