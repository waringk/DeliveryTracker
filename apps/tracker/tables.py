import django_tables2 as tables
from django.utils.safestring import mark_safe

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
            record) + " " + self.linkify('<br>Photo Details', record))

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
        sequence = ("photo", "created", "user",)
        fields = ("photo", "created", "user",)
        exclude = ("id",)
        empty_text = "No data available."
