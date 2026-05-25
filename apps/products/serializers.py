from rest_framework import serializers
from .models import Category, Product
from .services import create_product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model=Product
        fields=[
            'id',
            'category',
            'name',
            'slug',
            'description',
            'price',
            'stock',
            'is_available',
            'created_at',
        ]
    
class ProductWriteSerializer(serializers.ModelSerializer):
    category= serializers.PrimaryKeyRelatedField(
        queryset= Category.objects.all()
    )
    class Meta:
        model= Product
        fields= [
            'id',
            'category',
            'name',
            'slug',
            'description',
            'price',
            'stock',
            'is_available',
        ]
    def create(self, validated_data):
        return create_product(validated_data)