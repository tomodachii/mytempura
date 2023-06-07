from rest_framework.views import APIView
from api.middlewares import RouteAuthenticationByJWT
from django.http import JsonResponse
from rest_framework import status
from drf_spectacular.utils import extend_schema
from keywordrecognition.serializers import KeywordResponseSerializer, KeywordCreateSerializer, KeywordUpdateSerializer
from keywordrecognition.models import Keyword, ElizaBot
from keywordrecognition.enums import ELIZA_BOT_EXCEPTION, KEYWORD_EXCEPTION
from api.serializers import NotificationSerializer


class KeywordDetailAPI(APIView):
    authentication_classes = [RouteAuthenticationByJWT]
    permission_classes = ()

    @extend_schema(responses={200: KeywordResponseSerializer}, tags=['eliza-bot-keyword'])
    def get(self, request, id):
        try:
            keyword = Keyword.objects.get(id=id)
            if keyword.bot.owner != request.user:
                return JsonResponse({'message': ELIZA_BOT_EXCEPTION.PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN)
            return JsonResponse(KeywordResponseSerializer(instance=keyword).data, status=status.HTTP_200_OK)
        except Keyword.DoesNotExist:
            return JsonResponse({'message': KEYWORD_EXCEPTION.KEYWORD_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @ extend_schema(request=KeywordUpdateSerializer, responses={200: KeywordResponseSerializer}, tags=['eliza-bot-keyword'])
    def put(self, request, id):
        try:
            keyword = Keyword.objects.get(id=id)
            if keyword.bot.owner != request.user:
                return JsonResponse({'message': ELIZA_BOT_EXCEPTION.PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN)
            serializer = KeywordUpdateSerializer(instance=keyword, data=request.data, partial=True)
            if serializer.is_valid():
                updated_eliza_bot = serializer.save()
                return JsonResponse(KeywordResponseSerializer(instance=updated_eliza_bot).data, status=status.HTTP_200_OK)
        except Keyword.DoesNotExist:
            return JsonResponse({'message': KEYWORD_EXCEPTION.KEYWORD_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @ extend_schema(responses={200: NotificationSerializer}, tags=['eliza-bot-keyword'])
    def delete(self, request, id):
        try:
            keyword = Keyword.objects.get(id=id)
            if keyword.bot.owner != request.user:
                return JsonResponse({'message': ELIZA_BOT_EXCEPTION.PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN)
            keyword.delete()
            return JsonResponse(NotificationSerializer({'message': "success"}).data, status=status.HTTP_200_OK)
        except Keyword.DoesNotExist:
            return JsonResponse({'message': str(KEYWORD_EXCEPTION.KEYWORD_NOT_EXIST)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class KeywordAPI(APIView):
    authentication_classes = [RouteAuthenticationByJWT]
    permission_classes = ()

    @extend_schema(responses={200: KeywordResponseSerializer(many=True)}, tags=['eliza-bot-keyword'])
    def get(self, request, bot_id):
        try:
            bot = ElizaBot.objects.get(id=bot_id)
            keywords = Keyword.objects.filter(bot=bot)
            return JsonResponse(KeywordResponseSerializer(keywords, many=True).data, status=status.HTTP_200_OK, safe=False)
        except ElizaBot.DoesNotExist:
            return JsonResponse({'message': ELIZA_BOT_EXCEPTION.ELIZA_BOT_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @ extend_schema(request=KeywordCreateSerializer, responses={200: KeywordResponseSerializer}, tags=['eliza-bot-keyword'])
    def post(self, request):
        try:
            serializer = KeywordCreateSerializer(data=request.data)
            if serializer.is_valid():
                bot = serializer.validated_data['bot']
                if bot.owner == request.user:
                    keyword = serializer.save()
                    return JsonResponse(KeywordResponseSerializer(keyword).data, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'message': ELIZA_BOT_EXCEPTION.PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN)
            else:
                return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
