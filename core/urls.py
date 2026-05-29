"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore

schema_view= get_schema_view(
    openapi.Info(
        title = "AI Ecommerce API",
        default_version= 'v1',
        description= "Ecommerce Backend APIs",
    ),
    public= True,
    permission_classes= [permissions.AllowAny],
    authentication_classes=[],
)

@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "AI Ecommerce Backend API is running 🚀",
        "version": "v1",
        "endpoints": {
            "admin":           "/admin/",
            "swagger docs":    "/swagger/",
            "redoc docs":      "/redoc/",
            "users":           "/api/users/",
            "products":        "/api/products/",
            "orders":          "/api/orders/",
            "recommendations": "/api/recommendations/",
            "chatbot":         "/api/chatbot/",
            "token":           "/api/token/",
            "token refresh":   "/api/token/refresh/",
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/recommendations/', include('apps.recommendations.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name= 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name= 'token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/chatbot/', include('apps.chatbot.urls')),
]
