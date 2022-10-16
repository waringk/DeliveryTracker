from django.views import generic

from .forms import UserRegisterForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.core.files.base import ContentFile

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from datetime import datetime

import json
import cv2
import numpy as np

from .models import Event

from django_tables2 import SingleTableView
from .tables import EventTable


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

    return HttpResponse('Upload successful')


# class EventListView(generic.ListView):
#     # Template for user to view all their events - Non-table format.
#     model = Event
#     context_object_name = 'event_list'
#     queryset = Event.objects.all()
#     template_name = "app-tracker/events_list.html"


class EventListView(SingleTableView):
    # Template for user to view all their events in a table format.
    model = Event
    table_class = EventTable
    template_name = 'app-tracker/events_list.html'


class EventDetailView(generic.DetailView):
    # Template for user to view an individual event.
    model = Event
    context_object_name = 'event'
    template_name = "app-tracker/event_detail.html"


