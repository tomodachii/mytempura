from rest_framework import authentication, exceptions
import logging
import os
from backend.services import firebase_service
from backend.models import Account
from backend.services import jwt_service


logger = logging.getLogger(__name__)
environment = os.environ.get('ENVIRONMENT', 'development')


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].replace('Bearer ', '')
            firebase_user = firebase_service.get_user(id_token=token)
            user, created = Account.objects.get_or_create(email=firebase_user.email, uid=firebase_user.uid)
            return (user, None)

        except (Account.DoesNotExist, KeyError, IndexError):
            raise exceptions.AuthenticationFailed('Invalid or missing token')

        except Exception as e:
            error_messages = {"jwt_token": {"detail": str(e)}}
            raise exceptions.APIException(error_messages)


class RouteAuthenticationByJWT(authentication.BaseAuthentication):
    """override the django base authentication by the custom authenticate"""

    def authenticate(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            decoded = jwt_service.decode(token.replace('Bearer ', ''))
            user = Account.objects.get(
                email=decoded['email'])
            return (user, None)

        except (Account.DoesNotExist, KeyError, IndexError):
            raise exceptions.AuthenticationFailed('Invalid or missing token')

        except Exception as e:
            error_messages = {"jwt_token": {"detail": str(e)}}
            raise exceptions.APIException(error_messages)
