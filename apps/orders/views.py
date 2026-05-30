from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .services import create_order
from .tasks import send_order_confirmation_email
from .models import Order, OrderItem, Cart, CartItem
from .serializers import OrderSerializer, CreateOrderSerializer
from .cart_serializers import CartSerializer, CartItemAddSerializer
from apps.products.models import Product


class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body= CreateOrderSerializer)
    def post(self, request):
        items = request.data.get('items')

        if not items:
            return Response(
                {"error": "No items provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(user=request.user)

        for item in items:

            product = Product.objects.get(id=item['product'])

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price
            )

        serializer = OrderSerializer(order)
        #send_order_confirmation_email.delay(order.id)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class AddToCartAPIView(APIView):
    permission_classes= [IsAuthenticated]

    @swagger_auto_schema(request_body=CartItemAddSerializer)
    def post(self, request):
        product_id= request.data.get('product')
        quantity= request.data.get('quantity', 1)
        print(product_id)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status= 404
            )
        cart, created = Cart.objects.get_or_create(user= request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product= product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        
        cart_item.save()

        return Response({
            "message": "Product added to cart",
            "product": product.name,
            "quantity": cart_item.quantity
        })

    
class CartAPIView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request):
        try:
            cart= Cart.objects.get(user=request.user)
            cart_items= CartItem.objects.filter(cart= cart)
            data= []
            for item in cart_items:
                data.append({
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "price": item.product.price,
                    "total_price": item.quantity * item.product.price 
                })
            return Response(data)
        except Cart.DoesNotExist:
            return Response({"message": "Cart is empty"}, status= 200)
        
# Create your views here.
