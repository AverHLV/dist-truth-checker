from django.db import models
from django.core.validators import RegexValidator
from config import constants


class Text(models.Model):
    """ Text model for truth checking """

    created = models.DateTimeField(auto_now_add=True)
    true_similarity = models.FloatField(default=-1)
    false_similarity = models.FloatField(default=-1)
    language = models.CharField(max_length=2, choices=(('ru', 'Russian'), ('uk', 'Ukrainian'), ('en', 'English')))
    headline = models.CharField(max_length=constants.headline_max_length)
    cleared_text = models.TextField(max_length=constants.text_max_length)

    message_id = models.CharField(
        max_length=constants.message_id_length, unique=True,
        validators=[
            RegexValidator(regex=r'^.{%s}$' % constants.message_id_length, message='Wrong message_id length.')
        ]
    )

    class Meta:
        db_table = 'texts'

    def __str__(self):
        return self.message_id

    def get_check_status(self, threshold=constants.status_threshold):
        """ Get topic modeling result """

        if self.true_similarity < self.false_similarity - threshold:
            return True

        return False

    def get_response_data(self):
        """ Get dictionary for api response """

        return {'message_id': self.message_id, 'check_result': self.get_check_status()}
