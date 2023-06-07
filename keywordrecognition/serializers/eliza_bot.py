from rest_framework import serializers
from backend.models import Account
from keywordrecognition.models import ElizaBot
from keywordrecognition.enums import FILE_EXCEPTION


class ElizaBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElizaBot
        fields = ['name', 'description']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'name', 'description']


class ElizaBotResponseSerializer(serializers.ModelSerializer):
    owner = AccountSerializer()

    class Meta:
        model = ElizaBot
        fields = ['id', 'name', 'description', 'owner']


class ElizaBotLoadTxtSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        if value:
            if not value.name.endswith('.txt'):
                raise serializers.ValidationError(FILE_EXCEPTION.INVALID_FILE_EXTENSION_TXT)
            size_in_mb = value.size / (1024 * 1024)
            if size_in_mb > 2:
                raise serializers.ValidationError(FILE_EXCEPTION.FILE_TOO_LARGE)
        return value


class ElizaBotInputMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)


class ElizaBotGenerateResponseSerializer(serializers.Serializer):
    response = serializers.CharField(required=True)
