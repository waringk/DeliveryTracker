from django.urls import path

# from apps.tracker.views import HomePageView, SignUpView, upload_frame
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.HomePageView.as_view(), name='home'),
    path('uploadFrame/', views.upload_frame, name='uploadFrame'),
    # path('uploadFrame/', upload_frame, name='uploadFrame'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<int:pk>', views.EventDetailView.as_view(),
         name='event_detail'),
    path('photos/', views.PhotoListView.as_view(), name='photos'),
    path('photos/<int:pk>', views.PhotoDetailView.as_view(),
         name='photo_detail'),
]
