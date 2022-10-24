import itertools

import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_tables2 import TemplateColumn

from .models import Event


class PhotoTable(tables.Table):
    # Creates the columns for model attributes
    id = tables.Column()
    selected_photos = tables.Column(empty_values=(), verbose_name='')
    photo = tables.Column()
    created = tables.Column()
    user = tables.Column()
    autocheck = False
    delete = TemplateColumn(
        '<a href="{% url "delete_photo" record.id %}" type="submit" class="btn '
        'btn-success">Delete</a>', verbose_name='')

    def __init__(self, *args, **kwargs):
        super(PhotoTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_selected_photos(self, record):
        return mark_safe(
            '<input type="checkbox" onchange="photoButtonChangeHandler(this)" name="selected_photos'
            + str(next(self.counter)) + '" value="' + str(record.id) + '" />')

    def render_photo(self, value, record):
        # Render the photo as a linkable image in the column
        return mark_safe(self.linkify(
            "<img src='" + value.url + "' class='img-thumbnail'  />",
            record) + " " + self.linkify('<br>Photo Details', record))

    def linkify(self, text, record):
        # Render the photo link in the column to photo's details page
        return mark_safe(f"<a href=" + str(record.id) + " >" + text + "</a>")

    class Meta:
        model = Event
        template_name = "django_tables2/bootstrap4.html"
        sequence = ("selected_photos", "photo", "created", "user")
        fields = ("photo", "created", "user", "selected_photos")
        exclude = ("id",)
        empty_text = "No data available."
        # Have headers stay at the top
        attrs = {"thead": {"class": "bg-body sticky-top"}}


class EventTable(tables.Table):
    # Creates the columns for model attributes
    id = tables.Column()
    selected_events = tables.Column(empty_values=(), verbose_name='')
    photo = tables.Column()
    created = tables.Column()
    user = tables.Column()
    autocheck = False
    delete = TemplateColumn(
        '<a href="{% url "delete_event" record.id %}" type="submit" class="btn '
        'btn-success">Delete</a>', verbose_name='')

    def __init__(self, *args, **kwargs):
        super(EventTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_selected_events(self, record):
        return mark_safe(
            '<input type="checkbox" onchange="eventButtonChangeHandler(this)" name="selected_events'
            + str(next(self.counter)) + '" value="' + str(record.id) + '" />')

    def render_photo(self, value, record):
        # Render the photo as a linkable image in the column
        return mark_safe(self.linkify(
            "<img src='" + value.url + "' class='img-thumbnail' />",
            record) + " " + self.linkify('<br>Event Details', record))

    def linkify(self, text, record):
        # Render the event link in the column to events' details page
        return mark_safe(f"<a href=" + str(record.id) + " >" + text + "</a>")

    class Meta:
        model = Event
        template_name = "django_tables2/bootstrap4.html"
        sequence = ("selected_events", "photo", "created", "user")
        fields = ("photo", "created", "user", "selected_events")
        exclude = ("id",)
        empty_text = "No data available."
        # Have headers stay at the top
        attrs = {"thead": {"class": "bg-body sticky-top"}}
