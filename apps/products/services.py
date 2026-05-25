from .models import Product
from django.core.cache import cache


def create_product(validated_data):
    product= Product.objects.create(**validated_data)
    cache.delete('product_list')
    return product
