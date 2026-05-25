from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

User= get_user_model()

class UserProductInteraction(models.Model):
    INTERACTION_CHOICES= (
        ('view', 'View'),
        ('cart', 'Cart'),
        ('purchase', 'Purchase'),
    )

    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete= models.CASCADE)
    interaction_type= models.CharField(
        max_length= 20,
        choices= INTERACTION_CHOICES
    )
    created_at= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.interaction_type}"

# Create your models here.
