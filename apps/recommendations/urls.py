from django.urls import path
from .views import ProductRecommendationAPIView

urlpatterns=[
    path('<int:product_id>/', ProductRecommendationAPIView.as_view()),
]