from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        label=_('email address'),
        help_text=_('Required. You should provide a valid email address to sign up.')
    )

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
    bgcolor = forms.Field(widget=ColorPickerWidget, label=_('background color'))
