import json
from datetime import datetime

import cv2
import numpy as np
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, DeleteView
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig

from .forms import UserRegisterForm, DateForm, DeleteEventsForm, DeletePhotosForm,\
    UserDeviceForm, UserSettingsForm
from .models import Event, UserDevice, UserSettings
from .tables import EventTable, PhotoTable


class HomePageView(TemplateView):
    # Specify template name to use app level home.html.
    template_name = "app-tracker/home.html"


def signup(request):
    # Renders a registration page with the user registration and device
    # registration forms.
    if request.method == 'POST':
        print('hello world')
        # Use UserRegisterForm and UserDeviceForm for the signup view.
        form = UserRegisterForm(request.POST)
        device_form = UserDeviceForm(request.POST)
        settings_form = UserSettingsForm(request.POST)
        if form.is_valid() and device_form.is_valid() and settings_form.is_valid():
            print('1')
            user = form.save()

            # Create a device object, but not save it yet
            device = device_form.save(commit=False)
            device.user = user
            print('value 1', device.uuid)
            print('value 2', device.user.pk)
            device.save()

            print('abc1')
            settings_form.instance.id = user.pk
            settings = settings_form.save(commit=False)
            print('abc2')
            #settings_form.uuid = device
            settings.save()


            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print(username)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
        device_form = UserDeviceForm()
        settings_form = UserSettingsForm()

    context = {"form": form, "device_form": device_form, "settings_form": settings_form}
    return render(request, "registration/signup.html", context)


class CorrectUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    # Checks if the selected photo or event belongs
    # to the user.
    def test_func(self):
        event = self.get_object()
        return event.user == self.request.user


class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    # Use the new password change template and redirects to
    # the password_success page after successfully changing password.
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_success")


class PasswordsResetView(PasswordResetView):
    # Creates the form to submit our email and sends the custom email
    # template with the password reset link.
    form_class = PasswordResetForm
    template_name = "registration/reset_password.html"
    subject_template_name = "registration/reset_password_subject.txt"
    email_template_name = "registration/reset_password_email.html"


class PasswordsResetDoneView(PasswordResetDoneView):
    # Redirects the user to a page that lets the user know that the
    # reset email was sent.
    template_name = "registration/reset_password_done.html'"


class PasswordsResetConfirmView(PasswordResetConfirmView):
    # Links to the reset password link in the email.
    form_class = SetPasswordForm
    template_name = "registration/reset_password_confirm.html"


class PasswordsResetCompleteView(PasswordResetCompleteView):
    # Redirects the user to the password reset success message page.
    template_name = "registration/reset_password_complete.html"


def password_success(request):
    # Renders the password_success template.
    return render(request, 'registration/password_success.html')


def reset_password(request):
    # Renders the reset_password template.
    return render(request, 'registration/reset_password.html')


def UserSettingsView(request, username):
    # View for User to update their User Settings

    # If the user updates their info, submit the entered form
    if request.method == 'POST':
        user = request.user
        user_form = UserSettingsForm(request.POST, instance=user)
        if user_form.is_valid():
            saved_user_settings = user_form.save()
            return redirect('/../user_settings/'+str(user.username))

    # Otherwise, fetch the user's personal info and device ID in the form
    try:
        user = get_user_model().objects.filter(username=username).first()
        if user:
            device_form = UserDeviceForm()
            form = UserSettingsForm(instance=user)
            return render(request, 'registration/user_settings.html', context={'form': form, 'device_form': device_form,
                                                                               'uuid': form.initial['uuid']})
    except User.DoesNotExist:
         raise Http404("Given user not found")
    return redirect("registration/user_settings.html")


@csrf_exempt
def upload_frame(request):
    if request.method == 'POST':
        # convert image
        data = json.loads(request.body)
        arrayFrame = np.asarray(data['arr'])
        ret, jpg_frame = cv2.imencode('.jpg', arrayFrame)
        content = ContentFile(jpg_frame.tobytes())

        # use UUID to verify device and locate user
        user_device = get_object_or_404(UserDevice, uuid=data['param'])
        user = get_object_or_404(User, pk=user_device.user.pk)

        # create new image instance and save in db
        eventInstance = Event(user=user)
        photoName = str(datetime.now()) + '.jpg'
        photoName = photoName.replace(" ", "_")
        photoName = photoName.replace(":", ".")
        eventInstance.photo.save(photoName, content, save=False)
        eventInstance.save()

        send_email(user.email, user.username)

    return HttpResponse('Upload successful')


class PhotoListView(LoginRequiredMixin, CreateView,
                    SingleTableView):
    # Renders a table with all the photos of a user. By default,
    # displays user's most recent uploaded date of photo(s).
    model = Event
    table_class = PhotoTable
    template_name = 'app-tracker/photos_list.html'

    # Get all the photos of the current user and add it to the table.
    def get(self, request):
        try:
            # Get all the tables of the current user
            table = PhotoTable(
                Event.objects.filter(user=self.request.user))
        # If there are no photos for the user, renders an empty event list
        except IndexError:
            table = PhotoTable(Event.objects.all())
        RequestConfig(request).configure(table)
        return render(request, self.template_name,
                      {"table": table})


class PhotoDetailView(CorrectUserMixin,
                      generic.DetailView):
    # Template for user to view an individual photo.
    model = Event
    context_object_name = 'event'
    template_name = "app-tracker/photo_detail.html"


class PhotosDeleteView(LoginRequiredMixin, CreateView,
                       SingleTableView,
                       SingleTableMixin):
    # Form view for deleting selected photos with checkbox
    form_class = DeletePhotosForm
    template_name = 'app-tracker/photos_list.html'
    table_class = PhotoTable

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            table = PhotoTable(Event.objects.filter(user=self.request.user))
            if form.is_valid():
                for item in request.POST:
                    if item.startswith('selected_photos'):
                        selected_photos = request.POST.get(item, None)
                        Event.objects.get(id=selected_photos).delete()
                return HttpResponseRedirect(f"../photos/", {'form': form})
            return render(request, "app-tracker/photos_list.html",
                          {"form": form, "table": table})


class PhotoDeleteView(CorrectUserMixin, DeleteView):
    # Delete view for deleting individual event
    template_name = 'app-tracker/delete.html'
    model = Event
    success_url = reverse_lazy("photos/")

    def get(self, request, pk):
        if request.method == 'GET':
            event = get_object_or_404(Event, pk=pk)
            event.delete()
            return HttpResponseRedirect('../../photos')
        return redirect(request, "app-tracker/photos_list.html")


class EventDetailView(CorrectUserMixin,
                      generic.DetailView):
    # Template for user to view an individual event.
    model = Event
    context_object_name = 'event'
    template_name = "app-tracker/event_detail.html"


class EventListView(LoginRequiredMixin, CreateView,
                    SingleTableView):
    # View for user to view their events in a table format
    # By Default - Displays user's most recent uploaded date of photo(s)
    model = Event
    table_class = EventTable
    template_name = 'app-tracker/events_list.html'
    form_class = DateForm

    def get(self, request):
        # Finds most recently uploaded photo(s) date by default
        today = datetime.now(None)
        try:
            # Initializes the date form with the most recent photo(s) date
            newest_event = Event.objects.filter().values('created')[:1]
            today = newest_event[0]['created'].date()
            form = DateForm(initial={'created': today})
            table = EventTable(
                Event.objects.filter(user=self.request.user).filter(
                    created__date=today))
        # If there are no photos for the user, renders an empty event list
        except IndexError:
            form = DateForm(initial={'created': today})
            table = EventTable(Event.objects.all())
        RequestConfig(request).configure(table)
        return render(request, self.template_name,
                      {"form": form, "table": table})


class EventsByDateFormView(LoginRequiredMixin, View,
                           SingleTableMixin):
    # Form view for selecting displayed Events by date with calendar widget
    form_class = DateForm
    initial = {'events': Event.objects.all()}
    template_name = 'app-tracker/events_list.html'

    def post(self, request, *args, **kwargs):
        # Post request for filtering Events by date
        form = self.form_class(request.POST)
        form.instance.user = request.user
        user_events = Event.objects.filter(user=self.request.user)
        if form.is_valid():
            date = form.cleaned_data['created']
            date_only = date.date()
            # If the submitted value is invalid, display the user's events
            if not date:
                return render(request, self.template_name,
                              {'form': user_events})
            # Otherwise, redirect the user to the selected day's events
            else:
                return HttpResponseRedirect(f"../events/" + str(date_only),
                                            {'form': form})
        return render(request, self.template_name, {'form': form})


class EventsByDateFormResultsView(LoginRequiredMixin,
                                  CreateView,
                                  SingleTableView):
    # Results of selecting Events by date with calendar widget
    redirect_field_name = 'redirect_to'
    form_class = DateForm
    model = Event
    table_class = EventTable
    template_name = 'app-tracker/events_list_by_date.html'

    def get(self, request, date):
        # Get request for filtering Events by date
        return self.events_by_date_results(request, date)

    def events_by_date_results(self, request, date):
        # Displays selected Events by date with calendar widget
        if request.method == 'GET':
            form = self.form_class(request.GET)
            form.instance.user = request.user
            # Initializes the date form with the most recently selected date
            form = DateForm(initial={'created': date})
            table = EventTable(
                Event.objects.filter(user=self.request.user).filter(
                    created__date=date))
            RequestConfig(request).configure(table)
            return render(request, "app-tracker/events_list_by_date.html",
                          {"form": form, "table": table})


class EventsDeleteView(LoginRequiredMixin, CreateView,
                       SingleTableView,
                       SingleTableMixin):
    # Form view for deleting selected events with checkbox
    form_class = DeleteEventsForm
    template_name = 'app-tracker/events_list.html'
    table_class = EventTable

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            table = EventTable(Event.objects.filter(user=self.request.user))
            if form.is_valid():
                for item in request.POST:
                    if item.startswith('selected_events'):
                        selected_events = request.POST.get(item, None)
                        Event.objects.get(id=selected_events).delete()
                return HttpResponseRedirect(f"../events/", {'form': form})
            return render(request, "app-tracker/events_list_by_date.html",
                          {"form": form, "table": table})


class EventDeleteView(CorrectUserMixin, DeleteView):
    # Delete view for deleting individual event
    template_name = 'app-tracker/delete.html'
    model = Event
    success_url = reverse_lazy("events/")

    def get(self, request, pk):
        if request.method == 'GET':
            event = get_object_or_404(Event, pk=pk)
            event.delete()
            return HttpResponseRedirect('../../events')
        return redirect(request, "app-tracker/events_list_by_date.html")


def send_email(user_email, user_name):
    # Send event notification to user
    emailMessage = render_to_string('app-tracker/email.html',
                                    {'username': user_name})
    email = EmailMessage(
        'New Event Notification',
        emailMessage,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    email.fail_silently = False
    email.send()
    return
