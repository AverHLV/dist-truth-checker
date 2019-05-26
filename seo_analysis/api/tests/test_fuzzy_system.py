from django.test import TestCase
from unipath import Path
from json import loads
from config import constants
from ..fuzzy_system import control_system


def load_test_data():
    test_data_path = Path(__file__).absolute().ancestor(2).child('json').child('test_data.json')

    with open(test_data_path, encoding=constants.load_encoding) as file:
        return loads(file.read())


test_data = load_test_data()


class FuzzySystemTest(TestCase):
    """ Test fuzzy system evaluate method """

    def setUp(self):
        self.system = control_system

    def test_evaluation(self):
        result = self.system.evaluate(test_data['FuzzySystemTest']['cleared_text'])
        self.assertEqual(round(result, 5), test_data['FuzzySystemTest']['result'])
