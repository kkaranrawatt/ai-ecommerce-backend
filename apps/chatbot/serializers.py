from rest_framework import serializers

class ChatbotMessageSerializer(serializers.Serializer):
    message = serializers.CharField(
        help_text= "Type your message here"
    )