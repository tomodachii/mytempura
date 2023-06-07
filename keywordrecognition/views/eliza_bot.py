from rest_framework.views import APIView
from api.middlewares import RouteAuthenticationByJWT
from django.http import JsonResponse
from rest_framework import status, parsers
from keywordrecognition.serializers import ElizaBotSerializer, ElizaBotResponseSerializer, ElizaBotLoadTxtSerializer, ElizaBotInputMessageSerializer, ElizaBotGenerateResponseSerializer
from api.serializers import NotificationSerializer
from drf_spectacular.utils import extend_schema
from keywordrecognition.tasks import eliza_save_txt_data
import io
from celery.result import AsyncResult
from keywordrecognition.services import ElizaService
from keywordrecognition.models import ElizaBot
from keywordrecognition.enums import ELIZA_BOT_EXCEPTION


class ElizaBotDetailAPI(APIView):
    authentication_classes = [RouteAuthenticationByJWT]
    permission_classes = ()

    @extend_schema(responses={200: ElizaBotResponseSerializer}, tags=['eliza-bot'])
    def get(self, request, id):
        try:
            eliza_bot = ElizaBot.objects.get(id=id)
            if eliza_bot.owner != request.user:
                return JsonResponse({'message': ELIZA_BOT_EXCEPTION.PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN)
            return JsonResponse(ElizaBotResponseSerializer(instance=eliza_bot).data, status=status.HTTP_200_OK)
        except ElizaBot.DoesNotExist:
            return JsonResponse({'message': ELIZA_BOT_EXCEPTION.ELIZA_BOT_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @ extend_schema(request=ElizaBotSerializer, responses={200: ElizaBotResponseSerializer}, tags=['eliza-bot'])
    def put(self, request, id):
        try:
            eliza_bot = ElizaBot.objects.get(id=id)
            if eliza_bot.owner != request.user:
                return JsonResponse({'message': ELIZA_BOT_EXCEPTION.PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN)
            serializer = ElizaBotSerializer(instance=eliza_bot, data=request.data, partial=True)
            if serializer.is_valid():
                updated_eliza_bot = serializer.save()
                return JsonResponse(ElizaBotResponseSerializer(instance=updated_eliza_bot).data, status=status.HTTP_200_OK)
        except ElizaBot.DoesNotExist:
            return JsonResponse({'message': ELIZA_BOT_EXCEPTION.ELIZA_BOT_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @ extend_schema(responses={200: NotificationSerializer}, tags=['eliza-bot'])
    def delete(self, request, id):
        try:
            eliza_bot = ElizaBot.objects.get(id=id)
            if eliza_bot.owner != request.user:
                return JsonResponse({'message': ELIZA_BOT_EXCEPTION.PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN)
            eliza_bot.delete()
            return JsonResponse(NotificationSerializer({'message': "success"}).data, status=status.HTTP_200_OK)
        except ElizaBot.DoesNotExist:
            return JsonResponse({'message': str(ELIZA_BOT_EXCEPTION.ELIZA_BOT_NOT_EXIST)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ElizaBotAPIView(APIView):
    authentication_classes = [RouteAuthenticationByJWT]
    permission_classes = ()

    @extend_schema(responses={200: ElizaBotResponseSerializer(many=True)}, tags=['eliza-bot'])
    def get(self, request):
        try:
            eliza_bots = ElizaBot.objects.filter(owner=request.user)
            return JsonResponse(ElizaBotResponseSerializer(eliza_bots, many=True).data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @ extend_schema(request=ElizaBotSerializer, responses={200: ElizaBotResponseSerializer}, tags=['eliza-bot'])
    def post(self, request):
        try:
            serializer = ElizaBotSerializer(data=request.data)
            if serializer.is_valid():
                # serializer.certificate = request.FILES['business_certificate']
                eliza_bot = serializer.save(owner=request.user)
                return JsonResponse(ElizaBotResponseSerializer(eliza_bot).data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ElizaBotLoadTxtAPIView(APIView):
    authentication_classes = [RouteAuthenticationByJWT]
    permission_classes = []
    parser_classes = [parsers.MultiPartParser]

    @ extend_schema(request=ElizaBotLoadTxtSerializer, tags=['eliza-bot'])
    def post(self, request, id):
        try:
            bot = ElizaBot.objects.get(id=id)
            if bot.owner != request.user:
                return JsonResponse({'message': ELIZA_BOT_EXCEPTION.PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN)

            serializer = ElizaBotLoadTxtSerializer(data=request.data)
            if serializer.is_valid():
                data = []
                byte_io_file = serializer.validated_data['file'].file
                byte_str = byte_io_file.read()
                txt_file = io.TextIOWrapper(io.BytesIO(byte_str))
                for line in txt_file:
                    data.append(line)
                task = eliza_save_txt_data.delay(data=data, bot_id=id)
                return JsonResponse({'task_id': task.task_id, 'status': task.status}, status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ElizaBot.DoesNotExist:
            return JsonResponse({'message': ELIZA_BOT_EXCEPTION.ELIZA_BOT_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ElizaBotLoadTxtStatusAPIView(APIView):
    authentication_classes = [RouteAuthenticationByJWT]
    permission_classes = []

    @ extend_schema(tags=['eliza-bot'])
    def get(self, request, bot_id, task_id):
        try:
            task_result = AsyncResult(task_id)
            if task_result.name == 'eliza-load-txt':
                result = {
                    "task_id": task_id,
                    "task_status": task_result.status,
                }
                return JsonResponse(result, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ElizaBotGenerateResponseAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(request=ElizaBotInputMessageSerializer, responses={200: ElizaBotGenerateResponseSerializer}, tags=['eliza-bot'])
    def post(self, request, id):
        try:
            serializer = ElizaBotInputMessageSerializer(data=request.data)
            if serializer.is_valid():
                bot = ElizaBot.objects.get(id=id)
                eliza_service = ElizaService(bot=bot)
                response = eliza_service.response(text=serializer.validated_data['message'])
                response_serializer = ElizaBotGenerateResponseSerializer(data={'response': response})
                if response_serializer.is_valid():
                    return JsonResponse(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'message': response_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ElizaBot.DoesNotExist:
            return JsonResponse({'message': ELIZA_BOT_EXCEPTION.ELIZA_BOT_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
