from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(label='بريد إلكتروني')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

class ColorPickerWidget(forms.TextInput):
    input_type = 'color'

class PreferencesForm(forms.Form):
    bgcolor = forms.Field(widget=ColorPickerWidget, label='لون الخلفية')

