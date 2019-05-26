from django.test import TestCase
from config import constants
from .models import TextsAdmin


class UserCreationTest(TestCase):
    """ Test of user token generation while instance creating """

    def setUp(self):
        TextsAdmin.objects.create_user('user1')

    def test_model_fields(self):
        user = TextsAdmin.objects.get_by_natural_key('user1')
        self.assertTrue(len(user.token) == constants.token_length)
