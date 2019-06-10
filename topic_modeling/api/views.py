from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from os import environ
from .models import Text
from .serializers import CheckRequestSerializer, CheckResponseSerializer
from .helpers import lda_models, ref_messages

if environ['DJANGO_SETTINGS_MODULE'] == 'config.settings.production':
    from config.connector import cluster_connector
else:
    cluster_connector = None


class ModelingResult(APIView):
    """ Get Text object by message_id """

    @staticmethod
    def get(_request, message_id):
        try:
            text = Text.objects.get(message_id=message_id)

        except Text.DoesNotExist:
            return Response({'detail': 'Text with specified message_id not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CheckResponseSerializer(data=text.get_response_data())
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckText(APIView):
    """ Create Text instance, perform topic modeling and return results """

    @staticmethod
    def post(request):
        if cluster_connector is not None:
            if not cluster_connector.is_writable():
                return Response(
                    {'detail': 'Service is in read-only mode.'}, status=status.HTTP_409_CONFLICT,
                    content_type='application/json'
                )

        serializer = CheckRequestSerializer(data=request.data)

        if serializer.is_valid():
            text = Text(**serializer.validated_data)
            text.true_similarity = lda_models[text.language].compute_similarity([text.headline], [text.cleared_text])

            text.false_similarity = lda_models[text.language].compute_similarity(
                [ref_messages[text.language]['cleared_text']],
                [text.cleared_text]
            )

            text.save()

            serializer = CheckResponseSerializer(data=text.get_response_data())
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
