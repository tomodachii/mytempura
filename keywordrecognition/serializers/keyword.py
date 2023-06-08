from rest_framework import serializers
from keywordrecognition.models import Keyword, ElizaBot


class ElizaBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElizaBot
        fields = ["id", "name", "description"]


class KeywordCreateSerializer(serializers.ModelSerializer):
    bot = serializers.PrimaryKeyRelatedField(
        queryset=ElizaBot.objects.all(), required=True
    )

    class Meta:
        model = Keyword
        fields = ["bot", "word", "weight"]


class KeywordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["word", "weight"]


class KeywordResponseSerializer(serializers.ModelSerializer):
    bot = ElizaBotSerializer()

    class Meta:
        model = Keyword
        fields = ["id", "word", "weight", "bot"]
