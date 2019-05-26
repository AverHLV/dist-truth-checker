from django.test import TestCase
from unipath import Path
from json import loads
from config import constants
from ..helpers import lda_models, ref_messages


def load_test_data():
    test_data_path = Path(__file__).absolute().ancestor(2).child('json').child('test_data.json')

    with open(test_data_path, encoding=constants.load_encoding) as file:
        return loads(file.read())


test_data = load_test_data()


class LDAPredictionTest(TestCase):
    """
    Test built LDA models by similar and different texts,
    scores of similar texts should be smaller than score of different texts
    """

    def setUp(self):
        self.lda_uk = lda_models['uk']

    def test_lda_predictions(self):
        uk_similar_value = self.lda_uk.compute_similarity(
            [test_data['LDAPredictionTest']['uk_headline']],
            [test_data['LDAPredictionTest']['uk_cleared_text']]
        )

        uk_different_value = self.lda_uk.compute_similarity(
            [ref_messages['uk']['cleared_text']],
            [test_data['LDAPredictionTest']['uk_cleared_text']]
        )

        self.assertTrue(uk_similar_value < uk_different_value)
