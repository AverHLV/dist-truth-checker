from rest_framework.serializers import ModelSerializer, BooleanField
from .models import Text


class CheckRequestSerializer(ModelSerializer):
    class Meta:
        model = Text
        fields = 'message_id', 'language', 'headline', 'cleared_text'


class CheckResponseSerializer(ModelSerializer):
    check_result = BooleanField()

    class Meta:
        model = Text
        fields = 'message_id', 'check_result'
