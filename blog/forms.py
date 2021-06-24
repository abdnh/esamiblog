from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import User


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(label='بريد إلكتروني')

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

