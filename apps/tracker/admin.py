from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'photo', 'user']
    list_filter = ['created', 'user']
    raw_id_fields = ['user']
    date_hierarchy = 'created'
    ordering = ['-created']
