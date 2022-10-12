from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    # Add an email field to the UserRegisterForm class.
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]
