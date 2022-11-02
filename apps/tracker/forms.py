from crispy_forms.bootstrap import Modal
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Button
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Event, UserDevice, UserSettings


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

    def __init__(self, *args, **kwargs):
        # Uses django-crispy-forms FormHelper to render form, submit & post method
        super(UserDeviceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.helper.form_method = 'POST'


class UserSettingsForm(forms.ModelForm):
    # Form for storing User's personal information and User's device ID
    first_name = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    uuid = forms.CharField(max_length=36, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        # Uses django-crispy-forms FormHelper to render form, submit & post method
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.helper.form_method = 'POST'

        # Get the current user's info from User model
        found_user = get_object_or_404(User, id=self.instance.id)

        if found_user:
            # Get the user's personal information
            self.initial['first_name'] = found_user.first_name
            self.initial['last_name'] = found_user.last_name

            # Get the current user's device ID
            try:
                self.initial['uuid'] = UserDevice.objects.get(user_id=self.instance.id).uuid
            except UserDevice.DoesNotExist:
                raise Http404("Given device not found")

    class Meta:
        model = UserSettings
        fields = ('first_name', 'last_name', 'uuid',)

    def save(self, *args, **kwargs):
        # Overrides save method to obtain/combine User Model & User Device Model info
        settings = super(UserSettingsForm, self).save(commit=False)

        # Get the current user's current device ID
        try:
            found_device = UserDevice.objects.get(user_id=self.instance.id)
            form_device = found_device
        except UserDevice.DoesNotExist:
            # new_device = UserDevice()
            raise Http404("Given device not found")

        # Get the form entered device ID
        form_device.uuid = self.cleaned_data.get('uuid')
        form_device.user_id = self.instance.id
        form_device.save()

        # Get the form entered user's personal info
        self.instance.first_name = self.cleaned_data.get('first_name')
        self.instance.last_name = self.cleaned_data.get('last_name')

        try:
            found_user_settings = UserSettings.objects.get(user_id=self.instance.id)
            form_user_settings = found_user_settings
        except UserSettings.DoesNotExist:
            # new_user_settings = UserSettings()
            raise Http404("Given user not found")

        # Get the form entered device and user info
        form_user_settings.device_id = form_device.id
        form_user_settings.user_id = self.instance.id
        form_user_settings.save()
        settings.save()
        return settings


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
