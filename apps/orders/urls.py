from django.urls import path
from .views import (
    CreateOrderAPIView,
    AddToCartAPIView,
    CartAPIView)

urlpatterns = [
    path('create/', CreateOrderAPIView.as_view()),
    path('cart/add/', AddToCartAPIView.as_view()),
    path('cart/', CartAPIView.as_view()),
]
