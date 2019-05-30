from django.test import TestCase
from config import constants
from .test_fuzzy_system import test_data
from ..models import Text


class TextCreationTest(TestCase):
    """ Test Text model object creation """

    def setUp(self):
        Text.objects.create(
            message_id=test_data['TextCreationTest']['message_id'],
            language=test_data['TextCreationTest']['language'],
            headline=test_data['TextCreationTest']['headline'],
            cleared_text=test_data['TextCreationTest']['cleared_text']
        )

    def test_model_fields(self):
        text = Text.objects.get(message_id=test_data['TextCreationTest']['message_id'])

        self.assertTrue(len(text.message_id) == constants.message_id_length)
        self.assertTrue(text.fuzzy_mark == -1)
        self.assertEqual(text.headline, test_data['TextCreationTest']['headline'])
        self.assertEqual(text.cleared_text, test_data['TextCreationTest']['cleared_text'])
