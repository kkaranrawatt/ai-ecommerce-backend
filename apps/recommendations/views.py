from django.shortcuts import render
from rest_framework.views import APIView
from .services import get_recommended_products
from rest_framework.response import Response
#from django.db.models import Count
#from .models import ProductInteraction
#from .models import UserProductInteraction
from rest_framework.permissions import IsAuthenticated
#from django.db.models import Count, Case, When, IntegerField, Sum, Value
from apps.products.serializers import ProductReadSerializer
from .ai_recommender import get_ai_recommendations


class ProductRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, product_id):
        recommended_products= get_ai_recommendations(product_id)
        serializer= ProductReadSerializer(
            recommended_products,
            many=True
        )
        return Response(serializer.data)
# Create your views here.
