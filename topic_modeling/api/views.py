from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Text
from .serializers import CheckRequestSerializer, CheckResponseSerializer
from .helpers import lda_models, ref_messages


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


class ReadonlyResponse(APIView):
    """ Readonly response if primary db not alive """

    @staticmethod
    def get(_request):
        return Response({'detail': 'Service is in read-only mode'}, status=status.HTTP_409_CONFLICT)
