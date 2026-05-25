from django.urls import path
from .views import AIProductSearchAPIView, ProductListCreateAPIView, ProductDetailAPIView, ProductSearchAPIView, ProductListAPIView

urlpatterns=[
    #path('', ProductListCreateAPIView.as_view(), name='product-list'),
    #path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('',ProductListAPIView.as_view()),
    path('search/', ProductSearchAPIView.as_view()),
    path('ai-search/', AIProductSearchAPIView.as_view(), name='ai-search'),
]