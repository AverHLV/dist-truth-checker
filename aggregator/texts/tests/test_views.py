from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from config import constants
from .test_models import test_data
from ..views import TextsView, StartCheck
from ..models import Text


class TextsViewTest(TestCase):
    """ Test TextsView view by get request """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()

        Text.objects.create(
            headline=test_data['TextsViewTest']['headline'],
            raw_text=test_data['TextsViewTest']['raw_text'],
            language='en',
            cleared_text='*' * constants.text_min_length,
            cleared_headline='*' * constants.headline_min_length
        )

    def test_page(self):
        request = self.factory.get('/')
        request.user = self.user
        response = TextsView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context_data['texts'])
        self.assertIsInstance(response.context_data['texts'].first(), Text)


class StartCheckTest(TestCase):
    """ Test StartCheck view by get and post requests """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()

    def test_form_get(self):
        request = self.factory.get('/check')
        request.user = self.user
        response = StartCheck.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_form_post(self):
        request = self.factory.post(
            '/check',
            data={
                'headline': test_data['StartCheckTest']['headline'],
                'raw_text': test_data['StartCheckTest']['raw_text']
            }
        )

        request.user = self.user
        response = StartCheck.as_view()(request)

        self.assertEqual(response.status_code, 302)
