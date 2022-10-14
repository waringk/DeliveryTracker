from django.urls import path
from .views import upload_frame

urlpatterns = [
    path('uploadFrame/', upload_frame, name='uploadFrame'),
]
