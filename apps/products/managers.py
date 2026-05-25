from django.db import models

class ProductManager(models.Manager):
    def available(self):
        return self.filter(is_available = True)
    
    def in_stock(self):
        return self.filter(stock__gt = 0)