# from django.db import models
# from django.contrib.auth.models import User
#
#
# class Event(models.Model):
#     photo = models.ImageField(upload_to='images/')
#     created = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.photo)
#
#     class Meta:
#         get_latest_by = "upload_date"
