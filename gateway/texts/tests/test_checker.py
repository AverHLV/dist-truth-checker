from django.test import TestCase
from .test_models import test_data
from ..checker import CorrChecker


class CorrCheckerTest(TestCase):
    """ Test correctness checking for all supported languages """

    def test_text_correctness(self):
        checker = CorrChecker()

        self.assertTrue(checker(test_data['CorrCheckerTest']['text_ru']) is not None)
        self.assertTrue(checker(test_data['CorrCheckerTest']['text_en']) is not None)
        self.assertTrue(checker(test_data['CorrCheckerTest']['text_uk']) is not None)
        self.assertTrue(checker(test_data['CorrCheckerTest']['wrong_text_ru']) is None)
        self.assertTrue(checker(test_data['CorrCheckerTest']['wrong_text_uk']) is None)
