from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import ChatbotMessageSerializer
from .services import chatbot_response

class ChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChatbotMessageSerializer)
    def post(self, request):
        message= request.data.get('message')
        if not message:
            return Response({"error": "Message required"}, status=400)
        response= chatbot_response(message)
        return Response(response)

#  Create your views here.
