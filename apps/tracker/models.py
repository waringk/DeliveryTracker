from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Event(models.Model):
    photo = models.ImageField(upload_to='images/')
    created = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.photo)

    class Meta:
        get_latest_by = "upload_date"
        app_label = 'tracker'

    objects = models.Manager()
