import itertools

import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_tables2 import TemplateColumn

from .models import Event


class PhotoTable(tables.Table):
    # Creates the columns for model attributes
    id = tables.Column()
    photo = tables.Column()
    created = tables.Column()
    user = tables.Column()

    def render_photo(self, value, record):
        # Render the photo as a linkable image in the column
        return mark_safe(self.linkify(
            "<img src='" + value.url + "' class='img-fluid'  />",
            record) + " " + self.linkify('<br>Event Details', record))
        #return mark_safe(self.linkify(
        #    "<img src='" + value.url + "' width='480' height='200' />",
        #    record) + " " + self.linkify('<br>Event Details', record))

    def linkify(self, text, record):
        # Render the event link in the column to events' details page
        return mark_safe(f"<a href=" + str(record.id) + " >" + text + "</a>")

    class Meta:
        model = Event
        template_name = "django_tables2/bootstrap4.html"
        sequence = ("photo", "created", "user",)
        fields = ("photo", "created", "user",)
        exclude = ("id",)
        empty_text = "No data available."


class EventTable(tables.Table):
    # Creates the columns for model attributes
    id = tables.Column()
    photo = tables.Column()
    created = tables.Column()
    user = tables.Column()
    selected_events = tables.Column(empty_values=())

    def __init__(self, *args, **kwargs):
        super(EventTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_selected_events(self, record):
        return mark_safe('<input type="checkbox" name="selected_events'+str(next(self.counter))+'" value="' + str(record.id)+'"')

    def render_photo(self, value, record):
        # Render the photo as a linkable image in the column
        return mark_safe(self.linkify(
            "<img src='" + value.url + "' class='img-fluid' />",
            record) + " " + self.linkify('<br>Event Details', record))

    def linkify(self, text, record):
        # Render the event link in the column to events' details page
        return mark_safe(f"<a href=" + str(record.id) + " >" + text + "</a>")

    class Meta:
        model = Event
        template_name = "django_tables2/bootstrap4.html"
        sequence = ("photo", "created", "user", "selected_events")
        fields = ("photo", "created", "user","selected_events")
        exclude = ("id",)
        empty_text = "No data available."
