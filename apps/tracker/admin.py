from django.contrib import admin

from .models import Event, UserDevice, UserSettings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'photo', 'user']
    list_filter = ['created', 'user']
    raw_id_fields = ['user']
    date_hierarchy = 'created'
    ordering = ['-created']


class UserDeviceInline(admin.StackedInline):
    model = UserDevice
    can_delete = False


class AccountsUserAdmin(UserAdmin):
    def add_view(self, *args, **kwargs):
        # UUID is not registered when creating a user
        self.inlines = []
        return super(AccountsUserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        # UUID can be registered to user after user is created
        self.inlines = [UserDeviceInline]
        return super(AccountsUserAdmin, self).change_view(*args, **kwargs)

    inlines = [UserDeviceInline]


admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)
admin.site.register(UserSettings)