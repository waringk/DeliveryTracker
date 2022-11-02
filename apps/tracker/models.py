from django.contrib.auth.models import User
from django.db import models
# from django.db.models.signals import post_save
from django.utils import timezone
# from django.dispatch import receiver


class Event(models.Model):
    photo = models.ImageField(upload_to='images/')
    created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.photo)

    class Meta:
        ordering = ['-created']
        get_latest_by = "upload_date"
        app_label = 'tracker'

    objects = models.Manager()


class UserDevice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # uuid = models.CharField(max_length=36, null=True, blank=True)
    uuid = models.CharField(max_length=36, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.username+'/'+self.uuid


# @receiver(post_save, sender=User)
# def create_user_device(sender, instance, created, **kwargs):
#     # if user successfully added to User table, create device
#     if created:
#         # To create a user device object
#         UserDevice.objects.get_or_create(user=instance)
#


