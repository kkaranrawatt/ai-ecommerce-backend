from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Product
from .serializers import (
    ProductReadSerializer,
    ProductWriteSerializer
    )
from .permissions import IsAdminOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductReadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .ai_search import semantic_search




# @method_decorator(cache_page(60), name='dispatch')
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset= Product.objects.available().select_related('category')
    permission_classes= [IsAdminOrReadOnly]

    filterset_fields= ['category', 'is_available']
    search_fields= ['name', 'description']
    ordering_fields= ['price', 'created_at']

    def get_queryset(self):
        #print("DATABASE HIT")
        return Product.objects.available().select_related('category')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductWriteSerializer
        return ProductReadSerializer
    
    def list(self, request, *args, **kwargs):
        cache_key= 'product_list'
        cached_data= cache.get(cache_key)
        if cached_data:
            print("CACHE HIT")
            return Response(cached_data)
        print("DATABASE HIT")
        queryset= self.get_queryset()
        serializer= self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data)
    

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset= Product.objects.available().select_related('category')
    permission_classes= [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductWriteSerializer
        return ProductReadSerializer
    
class ProductSearchAPIView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q')
        products= Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains= query) |
            Q(category__name__icontains= query)
        )
        serializer= ProductReadSerializer(products, many=True)
        return Response(serializer.data)

class ProductListAPIView(generics.ListAPIView):
    queryset= Product.objects.all().order_by('-created_at')
    serializer_class= ProductReadSerializer
    filter_backends= [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields= ['category']
    search_fields= ['name' ,'description']
    ordering_fields= ['price', 'created_at']

    def list(self, request, *args, **kwargs):
        cached_products= cache.get('products')
        if cached_products:
            print('FETCHED FROM CACHE')
            return Response(cached_products)
        print('FETCHED FROM DATABASE')
        queryset= self.filter_queryset(self.get_queryset())
        page= self.paginate_queryset(queryset)

        if page is not None:
            serializer= self.get_serializer(page, many=True)
            paginated_response= self.get_paginated_response(serializer.data)
            cache.set('products', paginated_response.data, timeout= 60)
            return paginated_response
        serializer= self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AIProductSearchAPIView(APIView):
    def get(self, request):
        query= request.GET.get('q')

        if not query:
            return Response({'error': 'Query paramter required'})
        products= semantic_search(query)
        serializer= ProductReadSerializer(products, many= True)
        return Response(serializer.data)
    