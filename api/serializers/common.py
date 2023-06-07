from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    message = serializers.CharField()
