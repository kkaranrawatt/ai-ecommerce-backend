from django.db import models
from .managers import ProductManager

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete = models.CASCADE,
        related_name='products'
    )

    name= models.CharField(max_length=255, unique=True)
    slug= models.SlugField(unique =True)

    description = models.TextField()
    price = models.DecimalField(
        max_digits= 10,
        decimal_places= 2
    )

    stock= models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = ProductManager()

    def __str__(self):
        return self.name

# Create your models here.
