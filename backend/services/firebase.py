import firebase_admin
from firebase_admin import credentials, auth
import json
import requests
from django.conf import settings
from backend.exceptions import FirebaseException
from backend.enums import FIREBASE_EXCEPTION

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": settings.FIREBASE_PROJECT_ID,
    "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
    "private_key": settings.FIREBASE_PRIVATE_KEY,
    "client_email": settings.FIREBASE_CLIENT_EMAIL,
    "client_id": settings.FIREBASE_CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": settings.FIREBASE_CLIENT_CERT_URL
})


class FireBaseService:
    def __init__(self, cred, web_api_key):
        self.default_app = firebase_admin.initialize_app(cred)
        self.web_api_key = web_api_key

    def get_user(self, id_token):
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            return auth.get_user(uid, app=None)
        except Exception as e:
            # raise Exception(FIREBASE_EXCEPTION.GET_USER_ERROR)
            raise e

    def get_user_by_email(self, email):
        try:
            user = auth.get_user_by_email(email)
            return user
        except Exception as e:
            # raise Exception(FIREBASE_EXCEPTION.CREATE_USER_ERROR)
            raise FirebaseException(FIREBASE_EXCEPTION.GET_USER_BY_EMAIL_ERROR, str(e))

    def create_user(self, data={}):
        try:
            # Check if email and password are present
            if "email" not in data or "password" not in data:
                raise ValueError("Email and password are required.")
            # Add optional fields if they are present
            # if "phone_number" not in data:
            #     data["phone_number"] = None
            if "display_name" not in data:
                data["display_name"] = None
            if "photo_url" not in data:
                data["photo_url"] = None
            if "disabled" not in data:
                data["disabled"] = False

            user = auth.create_user(
                email=data["email"],
                password=data["password"],
                phone_number=None,
                display_name=data["display_name"],
                photo_url=data["photo_url"],
                disabled=data["disabled"],
                app=None
            )
            return user
        except Exception as e:
            # raise Exception(FIREBASE_EXCEPTION.CREATE_USER_ERROR)
            raise FirebaseException(FIREBASE_EXCEPTION.CREATE_USER_ERROR, str(e))

    def create_custom_token(self, uid):
        try:
            custom_token = auth.create_custom_token(uid)
            return custom_token.decode('utf-8')
        except Exception as e:
            raise e

    def sign_in_with_email_and_password(self, email: str, password: str, return_secure_token: bool = True) -> dict:
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": return_secure_token
        })

        response = requests.post(rest_api_url,
                                 params={"key": self.web_api_key},
                                 data=payload)

        return response.json()


firebase_service = FireBaseService(cred=cred, web_api_key=settings.FIREBASE_WEB_API_KEY)
