from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('', views.HomePageView.as_view(), name='home'),
    path('uploadFrame/', views.upload_frame, name='uploadFrame'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<int:pk>', views.EventDetailView.as_view(), name='event_detail'),
    path('events_by_date/', views.EventsByDateFormView.as_view(), name='events_by_date'),
    path('events/<str:date>', views.EventsByDateFormResultsView.as_view(), name='events_by_date_results'),
    path('events_delete', views.EventsDeleteView.as_view(), name='events_delete'),
    path('photos/', views.PhotoListView.as_view(), name='photos'),
    path('photos/<int:pk>', views.PhotoDetailView.as_view(),name='photo_detail'),

]
