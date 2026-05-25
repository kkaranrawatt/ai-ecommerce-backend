from django.db import models
from django.conf import settings
from apps.products.models import Product
#from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status= models.CharField(
        max_length=20,
        choices= STATUS_CHOICES,
        default= 'pending'
    )

    total_price= models.DecimalField(
        max_digits=10,
        decimal_places= 2,
        default= 0
    )

    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum (
            item.product.price * item.quantity for item in self.items.all()
        )

    def __str__(self):
        return f"Order {self.id}"
    
class OrderItem(models.Model):
    order= models.ForeignKey(
        Order,
        on_delete= models.CASCADE,
        related_name= 'items'
    )
    product= models.ForeignKey(
        Product,
        on_delete= models.CASCADE
    )
    quantity= models.PositiveIntegerField(default=1)

    price= models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    def __str__(self):
        return f"{self.product.name}"
    
class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE
    )
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Cart"
    
class CartItem(models.Model):
    cart= models.ForeignKey(
        Cart,
        related_name= 'items',
        on_delete= models.CASCADE
    )
    product= models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity= models.PositiveIntegerField(default = 1)

    def __str__(self):
        return self.product.name

# Create your models here.
