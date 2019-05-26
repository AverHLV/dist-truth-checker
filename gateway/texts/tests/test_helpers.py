from django.test import TestCase
from .test_models import test_data
from ..helpers import form_services_data


class ServicesDataTest(TestCase):
    """ Test services data generation for displaying in text detail view """

    def setUp(self):
        self.responses = test_data['ServicesDataTest']['responses']
        self.responses_unavailable = test_data['ServicesDataTest']['responses_unavailable']

    def test_response(self):
        services_data = form_services_data(self.responses, necessary_code=200)
        self.assertDictEqual(services_data, test_data['ServicesDataTest']['data'])

    def test_response_unavailable(self):
        services_data = form_services_data(self.responses_unavailable, necessary_code=200)
        self.assertDictEqual(services_data, test_data['ServicesDataTest']['data_unavailable'])
