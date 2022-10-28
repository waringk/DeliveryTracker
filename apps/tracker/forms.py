from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Event, UserDevice


class UserRegisterForm(UserCreationForm):
    # Custom user registration field with email.
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        # Overrides the save method to add the email field before saving
        # to the database.
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class UserDeviceForm(forms.ModelForm):
    # Adds the UUID field to register a device in the User registration
    # form.
    uuid = forms.CharField(max_length=100,
                           help_text='Please enter your PYNQ-Z2 device ID.')

    class Meta:
        model = UserDevice
        fields = ('uuid',)


class DeletePhotosForm(forms.Form):
    # Adds checkboxes to Photos
    selected_photos = forms.BooleanField(required=False, initial=False)


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


class DeleteEventsForm(forms.Form):
    # Adds checkboxes to Events
    selected_events = forms.BooleanField(required=False, initial=False)
