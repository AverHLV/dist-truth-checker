from django.test import TestCase
from unipath import Path
from json import loads
from config import constants
from ..models import Text


def load_test_data():
    test_data_path = Path(__file__).absolute().ancestor(2).child('json').child('test_data.json')

    with open(test_data_path, encoding=constants.load_encoding) as file:
        return loads(file.read())


test_data = load_test_data()


class TextCreationTest(TestCase):
    """ Test Text model object creation """

    def setUp(self):
        Text.objects.create(
            headline=test_data['TextCreationTest']['headline'],
            raw_text=test_data['TextCreationTest']['raw_text'],
            language='en',
            cleared_text='*' * constants.text_min_length,
            cleared_headline='*' * constants.headline_min_length
        )

    def test_model_fields(self):
        text = Text.objects.get(raw_text=test_data['TextCreationTest']['raw_text'])

        self.assertTrue(len(text.cleared_text))
        self.assertTrue(len(text.language) == 2)
        self.assertTrue(len(text.message_id) == constants.message_id_length)


class TextLangTest(TestCase):
    """ Test language detection """

    def setUp(self):
        Text.objects.create(
            headline=test_data['TextLangTest']['headline_ru'],
            raw_text=test_data['TextLangTest']['raw_text_ru'],
            language='en',
            cleared_text='*' * constants.text_min_length,
            cleared_headline='*' * constants.headline_min_length
        )

        Text.objects.create(
            headline=test_data['TextLangTest']['headline_uk'],
            raw_text=test_data['TextLangTest']['raw_text_uk'],
            language='en',
            cleared_text='*' * constants.text_min_length,
            cleared_headline='*' * constants.headline_min_length
        )

        Text.objects.create(
            headline=test_data['TextLangTest']['headline_en'],
            raw_text=test_data['TextLangTest']['raw_text_en'],
            language='en',
            cleared_text='*' * constants.text_min_length,
            cleared_headline='*' * constants.headline_min_length
        )

    def test_language_detection(self):
        text_ru = Text.objects.get(raw_text=test_data['TextLangTest']['raw_text_ru'])
        text_uk = Text.objects.get(raw_text=test_data['TextLangTest']['raw_text_uk'])
        text_en = Text.objects.get(raw_text=test_data['TextLangTest']['raw_text_en'])

        self.assertEqual(text_ru.language, 'ru')
        self.assertEqual(text_uk.language, 'uk')
        self.assertEqual(text_en.language, 'en')


class TextClearTest(TestCase):
    """ Test text clear process """

    def setUp(self):
        Text.objects.create(
            headline=test_data['TextClearTest']['headline'],
            raw_text=test_data['TextClearTest']['raw_text'],
            language='en',
            cleared_text='*' * constants.text_min_length,
            cleared_headline='*' * constants.headline_min_length
        )

    def test_cleared_fields(self):
        text = Text.objects.get(raw_text=test_data['TextClearTest']['raw_text'])

        self.assertEqual(text.cleared_text, test_data['TextClearTest']['cleared_text'])
        self.assertEqual(text.cleared_headline, test_data['TextClearTest']['cleared_headline'])
