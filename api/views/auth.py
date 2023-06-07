from rest_framework.views import APIView
# from api.middlewares import FirebaseAuthentication
from django.http import JsonResponse
from rest_framework import status
from backend.models import Account
from api.serializers import SignUpSerializer, SignInSerializer, ObtainTokenResponseSerializer, AccountSerializer
from backend.enums import ACCOUNT_EXCEPTION
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema
from backend.services import jwt_service


class SignUpAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()
    # parser_classes = ()

    @extend_schema(request=SignUpSerializer, responses={200: ObtainTokenResponseSerializer})
    def post(self, request):
        data = request.data
        try:
            serializer = SignUpSerializer(data=data)
            if serializer.is_valid():
                account = serializer.save()
                token, refresh_token, payload = jwt_service.encode(AccountSerializer(instance=account).data)
                response_serializer = ObtainTokenResponseSerializer({
                    'token': token,
                    'refresh_token': refresh_token,
                    'payload': payload
                })
                return JsonResponse(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignInAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(request=SignInSerializer, responses={200: ObtainTokenResponseSerializer})
    def post(self, request):
        data = request.data
        try:
            serializer = SignInSerializer(data=data)
            if serializer.is_valid() and data:
                account = Account.objects.get(email=serializer.validated_data['email'])
                if check_password(serializer.validated_data['password'], account.password):
                    token, refresh_token, payload = jwt_service.encode(AccountSerializer(instance=account).data)
                    response_serializer = ObtainTokenResponseSerializer({
                        'token': token,
                        'refresh_token': refresh_token,
                        'payload': payload
                    })
                    return JsonResponse(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'message': "Password not correct"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return JsonResponse({'message': str(ACCOUNT_EXCEPTION.ACCOUNT_NOT_EXIST)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
