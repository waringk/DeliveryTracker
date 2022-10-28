from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('change_password/', views.PasswordsChangeView.as_view(
        template_name="registration/change_password.html")),
    path('password_success', views.password_success, name='password_success'),
    path('reset_password/',
         views.PasswordsResetView.as_view(
             template_name="registration/reset_password.html"),
         name="reset_password"),
    path('reset_password', views.reset_password, name='reset_password'),
    path('reset_password/done/',
         views.PasswordsResetDoneView.as_view(
             template_name="registration/reset_password_done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.PasswordsResetConfirmView.as_view(
        template_name="registration/reset_password_confirm.html"),
         name="reset_password_confirm"),
    path('reset_password_complete/', views.PasswordsResetCompleteView.as_view(
        template_name="registration/reset_password_complete.html"),
         name="password_reset_complete"),
    path('', views.HomePageView.as_view(), name='home'),
    path('uploadFrame/', views.upload_frame, name='uploadFrame'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<int:pk>/delete', views.EventDeleteView.as_view(),
         name='delete_event'),
    path('events/<int:pk>', views.EventDetailView.as_view(),
         name='event_detail'),
    path('events_by_date/', views.EventsByDateFormView.as_view(),
         name='events_by_date'),
    path('events/<str:date>', views.EventsByDateFormResultsView.as_view(),
         name='events_by_date_results'),
    path('events_delete', views.EventsDeleteView.as_view(),
         name='events_delete'),
    path('photos/', views.PhotoListView.as_view(), name='photos'),
    path('photos/<int:pk>', views.PhotoDetailView.as_view(),
         name='photo_detail'),
    path('photos/<int:pk>/delete', views.PhotoDeleteView.as_view(),
         name='delete_photo'),
    path('photos_delete', views.PhotosDeleteView.as_view(),
         name='photos_delete'),
]
