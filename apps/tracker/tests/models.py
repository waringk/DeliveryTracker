from django.test import TestCase
from tracker.models import Event, UserDevice
from django.contrib.auth.models import User
import json
import tempfile

# run tests for models: python manage.py test tracker.tests.models
# ** or run with coverage report **
# coverage run --source='tracker.tests.models' manage.py test tracker.tests.models
# get report: coverage report


class TestTrackerModels(TestCase):
    def create_user(self, username='tester', password='12345'):
        return User.objects.create_user(username=username, password=password)

    def create_event(self, photo, user):
        return Event.objects.create(photo=photo, user=user)

    def create_device(self, user, uuid='911396a7-de99-49e0-b23d-643f48f08348'):
        return UserDevice.objects.create(user=user, uuid=uuid)

    def test_create_user(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))

    def test_create_user_and_device_paired(self):
        user = self.create_user()
        device = UserDevice.objects.create(user=user)
        self.assertEqual(user, device.user)

    def test_create_event_with_temp_file(self):
        user = self.create_user()
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        event = self.create_event(photo=image, user=user)
        self.assertTrue(isinstance(event, Event))

    def test_create_event_via_post(self):
        user = self.create_user()
        self.create_device(user=user)
        frameList = [[[255, 0, 0], [255, 0, 0], [255, 0, 0]]]
        data = {'param': '911396a7-de99-49e0-b23d-643f48f08348',
                'arr': frameList}
        response = self.client.post('http://127.0.0.1:9595/uploadFrame/',
                                    json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
