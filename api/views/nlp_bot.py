from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status, parsers
from api.serializers import NLPBotUploadCSVSerializer
from drf_spectacular.utils import extend_schema
from nlp.services import UploadService
from nlp.models import NLPBot
from nlp.enums import NLP_BOT_EXCEPTION
import tempfile


class EntityUploadCSVAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [parsers.MultiPartParser]

    @extend_schema(request=NLPBotUploadCSVSerializer, tags=["nlp-bot"])
    def post(self, request, bot_id):
        try:
            bot = NLPBot.objects.get(id=bot_id)
            # if bot.owner != request.user:
            #     return JsonResponse(
            #         {"message": NLP_BOT_EXCEPTION.PERMISSION_ERROR},
            #         status=status.HTTP_403_FORBIDDEN,
            #     )

            serializer = NLPBotUploadCSVSerializer(data=request.data)
            upload_service = UploadService(bot)
            if serializer.is_valid():
                csv_file = serializer.validated_data["file"].file
                with tempfile.NamedTemporaryFile(
                    suffix=".csv", delete=False
                ) as temp_file:
                    temp_file.write(csv_file.read())
                    temp_file.flush()
                    # Pass the file path to the upload_entities_from_csv method
                    upload_service.upload_entities_from_csv(temp_file.name)

                return JsonResponse(
                    {"task_id": "task.task_id", "status": "task.status"},
                    status=status.HTTP_200_OK,
                    safe=False,
                )
            else:
                return JsonResponse(
                    {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        except NLPBot.DoesNotExist:
            return JsonResponse(
                {"message": NLP_BOT_EXCEPTION.NLP_BOT_NOT_EXIST},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IntentUploadCSVAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [parsers.MultiPartParser]

    @extend_schema(request=NLPBotUploadCSVSerializer, tags=["nlp-bot"])
    def post(self, request, bot_id):
        try:
            bot = NLPBot.objects.get(id=bot_id)
            # if bot.owner != request.user:
            #     return JsonResponse(
            #         {"message": NLP_BOT_EXCEPTION.PERMISSION_ERROR},
            #         status=status.HTTP_403_FORBIDDEN,
            #     )

            serializer = NLPBotUploadCSVSerializer(data=request.data)
            upload_service = UploadService(bot)
            if serializer.is_valid():
                csv_file = serializer.validated_data["file"].file
                with tempfile.NamedTemporaryFile(
                    suffix=".csv", delete=False
                ) as temp_file:
                    temp_file.write(csv_file.read())
                    temp_file.flush()
                    # Pass the file path to the upload_entities_from_csv method
                    upload_service.upload_intents_from_csv(temp_file.name)

                return JsonResponse(
                    {"task_id": "task.task_id", "status": "task.status"},
                    status=status.HTTP_200_OK,
                    safe=False,
                )
            else:
                return JsonResponse(
                    {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        except NLPBot.DoesNotExist:
            return JsonResponse(
                {"message": NLP_BOT_EXCEPTION.NLP_BOT_NOT_EXIST},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResponseUploadCSVAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [parsers.MultiPartParser]

    @extend_schema(request=NLPBotUploadCSVSerializer, tags=["nlp-bot"])
    def post(self, request, bot_id):
        try:
            bot = NLPBot.objects.get(id=bot_id)
            # if bot.owner != request.user:
            #     return JsonResponse(
            #         {"message": NLP_BOT_EXCEPTION.PERMISSION_ERROR},
            #         status=status.HTTP_403_FORBIDDEN,
            #     )

            serializer = NLPBotUploadCSVSerializer(data=request.data)
            upload_service = UploadService(bot)
            if serializer.is_valid():
                csv_file = serializer.validated_data["file"].file
                with tempfile.NamedTemporaryFile(
                    suffix=".csv", delete=False
                ) as temp_file:
                    temp_file.write(csv_file.read())
                    temp_file.flush()
                    # Pass the file path to the upload_entities_from_csv method
                    upload_service.upload_responses_from_csv(temp_file.name)

                return JsonResponse(
                    {"task_id": "task.task_id", "status": "task.status"},
                    status=status.HTTP_200_OK,
                    safe=False,
                )
            else:
                return JsonResponse(
                    {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        except NLPBot.DoesNotExist:
            return JsonResponse(
                {"message": NLP_BOT_EXCEPTION.NLP_BOT_NOT_EXIST},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return JsonResponse(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
