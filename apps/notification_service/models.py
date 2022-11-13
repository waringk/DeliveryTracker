from notifications.base.models import AbstractNotification


class Notification(AbstractNotification):

    def __str__(self):
        print('x')
        return 'hello world'

    class Meta(AbstractNotification.Meta):
        abstract = False
        app_label = 'notification_service'
