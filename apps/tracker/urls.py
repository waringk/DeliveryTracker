from django.urls import path
#from apps.tracker.views import HomePageView, SignUpView, upload_frame
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.HomePageView.as_view(), name='home'),
    path('uploadFrame/', views.upload_frame, name='uploadFrame')
    #path('uploadFrame/', upload_frame, name='uploadFrame'),
]
