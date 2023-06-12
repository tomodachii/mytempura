from rest_framework import serializers
from backend.models import Account
from backend.enums import ACCOUNT_EXCEPTION
from django.contrib.auth.hashers import make_password


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ["id", "email", "password", "name", "description"]
        extra_kwargs = {
            "email": {"required": True, "allow_null": False},
            "password": {"required": True, "allow_null": False},
            "name": {"required": True, "allow_null": False},
        }

    def validate_email(self, value):
        if value:
            if Account.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    ACCOUNT_EXCEPTION.EMAIL_ALREADY_EXISTED
                )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        hashed_password = make_password(password)
        validated_data["password"] = hashed_password
        return super().create(validated_data)


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(allow_blank=True, trim_whitespace=False)


class TokenPayloadResponse(serializers.ModelSerializer):
    exp = serializers.FloatField()

    class Meta:
        model = Account
        fields = ["id", "name", "username", "email", "description", "exp"]


class ObtainTokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=False, required=False)
    refresh_token = serializers.CharField(allow_blank=False, required=False)
    payload = TokenPayloadResponse(required=False)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "email", "name", "description"]
