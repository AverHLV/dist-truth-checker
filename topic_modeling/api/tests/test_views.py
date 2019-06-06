from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .test_lda import test_data
from ..views import ModelingResult, CheckText, ReadonlyResponse
from ..models import Text


class ModelingResultTest(APITestCase):
    """ Test getting modeling results via get request """

    def setUp(self):
        self.factory = APIRequestFactory()

        self.response_data = {
            'message_id': test_data['ModelingResultTest']['message_id'],
            'check_result': test_data['ModelingResultTest']['check_result']
        }

        User.objects.create_user('user', 'email@email.com', 'password')

        Text.objects.create(
            message_id=test_data['ModelingResultTest']['message_id'],
            language=test_data['ModelingResultTest']['language'],
            headline=test_data['ModelingResultTest']['headline'],
            cleared_text=test_data['ModelingResultTest']['cleared_text']
        )

    def test_getting_result(self):
        request = self.factory.get('/api/result/{0}/'.format(self.response_data['message_id']))
        force_authenticate(request, user=User.objects.get(username='user'))
        response = ModelingResult.as_view()(request, self.response_data['message_id'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, self.response_data)


class CheckTextTest(APITestCase):
    """ Test text check post request """

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user('user', 'email@email.com', 'password')

    def test_text_checking(self):
        request = self.factory.post('/api/check/', data=test_data['CheckTextTest']['request_data'])
        force_authenticate(request, user=User.objects.get(username='user'))
        response = CheckText.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.data, test_data['CheckTextTest']['response_data'])


class ReadonlyTest(APITestCase):
    """ Test readonly state response code """

    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user('user', 'email@email.com', 'password')

    def test_readonly_response(self):
        request = self.factory.get('/api/check/readonly/')
        force_authenticate(request, user=User.objects.get(username='user'))
        response = ReadonlyResponse.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
