from django.test import TestCase
from django.contrib.auth.models import User
import json
import tracker.models
from tracker.views import *


# run tests : python manage.py test tracker.tests.urls
# run tests with coverage report :
# coverage run --source='tracker.tests.urls' manage.py test tracker.tests.urls
# get report : coverage report

URL = 'http://127.0.0.1:9595'


class TestTrackerURLs(TestCase):
    @staticmethod
    def create_user(username='tester', password='12345'):
        return User.objects.create_user(username=username, password=password)

    @staticmethod
    def create_event(photo, user):
        return tracker.models.Event.objects.create(photo=photo, user=user)

    @staticmethod
    def create_device(user, uuid='911396a7-de99-49e0-b23d-643f48f08348'):
        return tracker.models.UserDevice.objects.create(user=user, uuid=uuid)

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

    def test_admin_page(self):
        User.objects.create_superuser(username='admin',
                                      email='admin@gmail.com',
                                      password='capstone')
        self.client.login(username='admin', password='capstone')
        response = self.client.get(URL + '/admin/')
        self.assertEqual(response.status_code, 200)

    def test_home_page(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(URL + '/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get(URL + '/signup/')
        self.assertEqual(response.status_code, 200)

    def test_user_settings_page(self):
        # device must be created to successfully navigate to settings
        user = self.create_user()
        self.client.login(username='tester', password='12345')
        self.create_device(user=user)
        url = URL + '/user_settings/' + str(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_photos_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/photos/')
        self.assertEqual(response.status_code, 200)

    def test_events_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/events/')
        self.assertEqual(response.status_code, 200)

    def test_events_sort_photo_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/events/?sort=photo/')
        self.assertEqual(response.status_code, 200)

    def test_events_sort_created_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/events/?sort=created/')
        self.assertEqual(response.status_code, 200)

    def test_events_sort_user_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/events/?sort=user')
        self.assertEqual(response.status_code, 200)

    def test_events_by_date_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/events/2022-11-05')
        self.assertEqual(response.status_code, 200)

    def test_photos_sort_photo_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/photos/?sort=photo/')
        self.assertEqual(response.status_code, 200)

    def test_photos_sort_created_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/photos/?sort=created/')
        self.assertEqual(response.status_code, 200)

    def test_photos_sort_user_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/photos/?sort=user')
        self.assertEqual(response.status_code, 200)

    def test_notifications_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/inbox/notifications/')
        self.assertEqual(response.status_code, 200)

    def test_support_page(self):
        self.create_user_and_login()
        response = self.client.get(URL + '/support/')
        self.assertEqual(response.status_code, 200)

    def test_upload_frame_page_with_valid_id(self):
        user = self.create_user()
        self.create_device(user=user)
        frameList = [[[255, 0, 0], [255, 0, 0], [255, 0, 0]]]
        data = {'param': '911396a7-de99-49e0-b23d-643f48f08348',
                'arr': frameList}
        response = self.client.post(URL + '/uploadFrame/', json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_upload_frame_page_with_invalid_id(self):
        user = self.create_user()
        self.create_device(user=user)
        frameList = [[[255, 0, 0], [255, 0, 0], [255, 0, 0]]]
        data = {'param': '00000000-1111-2222-3333-444444444444',
                'arr': frameList}
        response = self.client.post(URL + '/uploadFrame/', json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
