import jwt
from django.conf import settings
import datetime


class JWTService:
    def __init__(self, secret, algorithm, exp, refresh_exp):
        self.jwt = jwt
        self.secret = secret
        self.algorithm = algorithm
        self.exp = exp
        self.refresh_exp = refresh_exp

    def encode(self, payload):
        return (
            jwt.encode(self.add_exp(payload), self.secret, algorithm=self.algorithm),
            jwt.encode(
                self.refresh_payload(payload), self.secret, algorithm=self.algorithm
            ),
            payload,
        )

    def decode(self, token):
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])

    def add_exp(self, payload):
        exp_time = datetime.datetime.now(tz=datetime.timezone.utc) + self.exp
        payload["exp"] = exp_time.timestamp()
        return payload

    def refresh_payload(self, payload):
        exp_time = datetime.datetime.now(tz=datetime.timezone.utc) + self.refresh_exp
        payload["exp"] = exp_time.timestamp()
        return payload


jwt_service = JWTService(
    settings.SECRET_KEY,
    settings.JWT_AUTH["JWT_ALGORITHM"],
    settings.JWT_AUTH["JWT_EXPIRATION_DELTA"],
    settings.JWT_AUTH["JWT_REFRESH_EXPIRATION_DELTA"],
)
