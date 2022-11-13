from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "notification_service"

    def ready(self):
        try:
            import apps.notification_service.signals
        except ImportError:
            pass