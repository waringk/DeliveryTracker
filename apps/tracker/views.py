import json
from datetime import datetime

import cv2
import numpy as np
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, DeleteView
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig

from .forms import UserRegisterForm, DateForm, DeleteEventsForm, \
    DeletePhotosForm
from .models import Event
from .tables import EventTable, PhotoTable


class HomePageView(TemplateView):
    # Specify template name to use app level home.html.
    template_name = "app-tracker/home.html"


class SignUpView(CreateView):
    # Use UserRegisterForm for the signup view.
    form_class = UserRegisterForm
    # Redirect the user to the login page after signing up successfully.
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class PasswordsChangeView(PasswordChangeView):
    # Use the new password change template and redirects to
    # the password_success page after successfully changing password.
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_success")


class PasswordsResetView(PasswordResetView):
    # Use the new reset password form and redirects to the login page
    # after successfully resetting the password.
    form_class = PasswordResetForm
    success_url = reverse_lazy("login")


def password_success(request):
    # Renders the password_success template.
    return render(request, 'registration/password_success.html')


def reset_password(request):
    # Renders the reset_password template.
    return render(request, 'registration/reset_password.html')


@csrf_exempt
def upload_frame(request):
    if request.method == 'POST':
        # convert image
        data = json.loads(request.body)
        arrayFrame = np.asarray(data['arr'])
        ret, jpg_frame = cv2.imencode('.jpg', arrayFrame)
        content = ContentFile(jpg_frame.tobytes())

        # get user
        try:
            # passing the pk is temporary, will update in later iteration
            user = User.objects.get(pk=data['param'])
        except ObjectDoesNotExist:
            HttpResponse.status_code = 404
            HttpResponse.reason_phrase = 'User not found. Register device'
            return HttpResponse()

        # create new image instance and save in db
        eventInstance = Event(user=user)
        photoName = str(datetime.now()) + '.jpg'
        photoName = photoName.replace(" ", "_")
        photoName = photoName.replace(":", ".")
        eventInstance.photo.save(photoName, content, save=False)
        eventInstance.save()

        send_email(user.email, user.username)

    return HttpResponse('Upload successful')


class PhotoListView(LoginRequiredMixin, SingleTableView):
    # Shows a list of photos
    model = Event
    table_class = PhotoTable
    template_name = 'app-tracker/photos_list.html'


class PhotoDetailView(LoginRequiredMixin, generic.DetailView):
    # Template for user to view an individual photo.
    model = Event
    context_object_name = 'event'
    template_name = "app-tracker/photo_detail.html"


class PhotosDeleteView(LoginRequiredMixin, CreateView, SingleTableView,
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


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
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


class EventDetailView(LoginRequiredMixin, generic.DetailView):
    # Template for user to view an individual event.
    model = Event
    context_object_name = 'event'
    template_name = "app-tracker/event_detail.html"


class EventListView(LoginRequiredMixin, CreateView, SingleTableView):
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


class EventsByDateFormView(LoginRequiredMixin, View, SingleTableMixin):
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


class EventsByDateFormResultsView(LoginRequiredMixin, CreateView,
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


class EventsDeleteView(LoginRequiredMixin, CreateView, SingleTableView,
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


class EventDeleteView(LoginRequiredMixin, DeleteView):
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
