from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import chatbot_response

class ChatbotAPIView(APIView):
    def post(self, request):
        message= request.data.get('message')
        if not message:
            return Response({"error": "Message required"})
        response= chatbot_response(message)
        return Response(response)

#  Create your views here.
