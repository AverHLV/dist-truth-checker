from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from uuid import uuid4
from config import constants
from .checker import CorrChecker

corr_checker = CorrChecker()


def create_text_id():
    """ Generate unique text identifier """

    message_id = uuid4().hex[:constants.message_id_length]

    try:
        while message_id in Text.objects.values_list('message_id', flat=True):
            message_id = uuid4().hex[:constants.message_id_length]

    except TypeError:
        # prevent migration errors if table does not exists

        return '1' * constants.message_id_length

    return message_id


class Text(models.Model):
    """ Text model for truth checking """

    created = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=2, choices=(('ru', 'Russian'), ('uk', 'Ukrainian'), ('en', 'English')))
    cleared_headline = models.CharField(max_length=constants.headline_max_length)
    cleared_text = models.TextField(max_length=constants.text_max_length)

    message_id = models.CharField(
        max_length=constants.message_id_length, unique=True, default=create_text_id,
        validators=[
            RegexValidator(regex=r'^.{%s}$' % constants.message_id_length, message='Wrong message_id length.')
        ]
    )

    headline = models.CharField(
        max_length=constants.headline_max_length,
        validators=[MinLengthValidator(constants.headline_min_length)]
    )

    raw_text = models.TextField(
        max_length=constants.text_max_length,
        validators=[MinLengthValidator(constants.text_min_length)],
        unique=True
    )

    class Meta:
        db_table = 'texts'

    def __str__(self):
        return self.raw_text[:constants.text_preview_length] + '...'

    def clean(self):
        """ Use CorrChecker to clear input text fields """

        results = corr_checker(self.headline)
        self.handle_check_errors(results)
        self.cleared_headline = results[0]

        results = corr_checker(self.raw_text)
        self.handle_check_errors(results)
        self.cleared_text = results[0]
        self.language = results[1]

    def get_post_request_data(self):
        """ Return dictionary with start checking post request necessary data """

        return {'message_id': self.message_id, 'language': self.language, 'headline': self.cleared_headline,
                'cleared_text': self.cleared_text}

    @staticmethod
    def handle_check_errors(results):
        """ Handle text clear exceptions """

        if results is None:
            raise ValidationError('Text correctness checking gives negative result.')

        if results == -1:
            raise ValidationError('Language detection error, please try another text.', code='ch1')

        if results == -2:
            raise ValidationError('Detected language is not supported.', code='ch2')
