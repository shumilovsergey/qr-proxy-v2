from rest_framework import serializers
from .models import Chats

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = ['chat_id', 'privat_url', 'public_url']

    def validate_chat_id(self, value):
        if Chats.objects.filter(chat_id=value).exists():
            raise serializers.ValidationError()
        return value