from django.test import TestCase
from django.contrib.auth.models import User
from apps.tracker import models
from django.urls import resolve, reverse
from apps.tracker.views import *


# python manage.py test tracker.tests.urls
# ** or run with coverage report **
# coverage run --source='tracker.tests.urls' manage.py test tracker.tests.urls
# coverage report


class TestTrackerURLs(TestCase):
    @staticmethod
    def create_user(username='tester', password='12345'):
        return User.objects.create_user(username=username, password=password)

    @staticmethod
    def create_event(photo, user):
        return models.Event.objects.create(photo=photo, user=user)

    @staticmethod
    def create_device(user, uuid='911396a7-de99-49e0-b23d-643f48f08348'):
        return models.UserDevice.objects.create(user=user, uuid=uuid)

    def create_user_and_login(self):
        self.create_user()
        self.client.login(username='tester', password='12345')

    def test_create_user_and_login(self):
        # login() returns True if credentials accepted & login was successful.
        self.create_user()
        login = self.client.login(username='tester', password='12345')
        self.assertTrue(login)

    def test_login_invalid_username(self):
        self.create_user()
        login = self.client.login(username='tested', password='12345')
        self.assertFalse(login)

    def test_login_invalid_password(self):
        self.create_user()
        login = self.client.login(username='tester', password='01234')
        self.assertFalse(login)

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, models.signup)

    def test_password_success_url_is_resolved(self):
        url = reverse('password_success')
        self.assertEqual(resolve(url).func, models.password_success)

    def test_home_page(self):
        response = self.client.get('http://127.0.0.1:9595/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('http://127.0.0.1:9595/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get('http://127.0.0.1:9595/signup/')
        self.assertEqual(response.status_code, 200)

    def test_user_settings_page(self):
        # device must be created to successfully navigate to settings
        user = self.create_user()
        self.client.login(username='tester', password='12345')
        self.create_device(user=user)
        url = 'http://127.0.0.1:9595/user_settings/'+str(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_photos_page(self):
        self.create_user_and_login()
        response = self.client.get('http://127.0.0.1:9595/photos/')
        self.assertEqual(response.status_code, 200)

    def test_events_page(self):
        self.create_user_and_login()
        response = self.client.get('http://127.0.0.1:9595/events/')
        self.assertEqual(response.status_code, 200)

    def test_events_sort_photo_page(self):
        self.create_user_and_login()
        response = self.client.get('http://127.0.0.1:9595/events/?sort=photo/')
        self.assertEqual(response.status_code, 200)

    def test_events_sort_created_page(self):
        self.create_user_and_login()
        response = self.client.get(
            'http://127.0.0.1:9595/events/?sort=created/')
        self.assertEqual(response.status_code, 200)

    def test_events_sort_user_page(self):
        self.create_user_and_login()
        response = self.client.get('http://127.0.0.1:9595/events/?sort=user')
        self.assertEqual(response.status_code, 200)

    def test_events_by_date_page(self):
        self.create_user_and_login()
        response = self.client.get('http://127.0.0.1:9595/events/2022-11-05')
        self.assertEqual(response.status_code, 200)

    def test_photos_sort_photo_page(self):
        self.create_user_and_login()
        response = self.client.get('http://127.0.0.1:9595/photos/?sort=photo/')
        self.assertEqual(response.status_code, 200)

    def test_photos_sort_created_page(self):
        self.create_user_and_login()
        response = self.client.get(
            'http://127.0.0.1:9595/photos/?sort=created/')
        self.assertEqual(response.status_code, 200)

    def test_photos_sort_user_page(self):
        self.create_user_and_login()
        response = self.client.get('http://127.0.0.1:9595/photos/?sort=user')
        self.assertEqual(response.status_code, 200)
