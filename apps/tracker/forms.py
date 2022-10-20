from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, Form
from .models import Event


class UserRegisterForm(UserCreationForm):
    # Add an email field to the UserRegisterForm class.
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]


class DateInput(forms.DateInput):
    # Date Input for selecting Events by date
    input_type = 'date'


class DateForm(ModelForm):
    # Calendar Form and Widget for selecting Events by date
    class Meta:
        model = Event
        fields = ['created']
        widgets = {
            'created': DateInput(),
        }