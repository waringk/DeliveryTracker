import json
from datetime import datetime

import cv2
import numpy as np
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig

from .forms import UserRegisterForm, DateForm
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
