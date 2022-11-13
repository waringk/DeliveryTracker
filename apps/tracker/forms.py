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


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        # Uses django-crispy-forms FormHelper to render form, submit & post method
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.helper.form_method = 'POST'

        # Set the initial values for the user info in the form
        try:
            found_user = User.objects.get(id=self.instance.id)
            self.instance.first_name = found_user.first_name
            self.instance.last_name = found_user.last_name
        except ObjectDoesNotExist:
            pass


class UserDeviceForm(forms.ModelForm):
    # Adds the UUID field to register a device in the User registration
    # form.
    uuid = forms.CharField(required=True, max_length=36,
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

        # Set the initial values for the user's device in the form
        try:
            found_device = UserDevice.objects.get(user_id=self.instance.id)
            self.initial['uuid'] = found_device.uuid
        except ObjectDoesNotExist:
            pass


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
