from rest_framework import serializers
from backend.enums import FILE_EXCEPTION


class NLPBotUploadCSVSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate_file(self, value):
        if value:
            if not value.name.endswith(".csv"):
                raise serializers.ValidationError(
                    FILE_EXCEPTION.INVALID_FILE_EXTENSION_CSV
                )
            size_in_mb = value.size / (1024 * 1024)
            if size_in_mb > 2:
                raise serializers.ValidationError(FILE_EXCEPTION.FILE_TOO_LARGE)
        return value


class NLPBotInputMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)


class NLPBotGenerateResponseSerializer(serializers.Serializer):
    response = serializers.CharField(required=True)


class NLPBotTrainModelSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
