from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product

@receiver(post_save, sender=Product)
def clear_product_cache_on_save(sender, instance, **kwargs):
    print('CACHE CLEARED AFTER SAVE')
    cache.delete('product_list')

@receiver(post_delete, sender=Product)
def clear_product_cache_on_delete(sender, instance, **kwargs):
    print('CACHE CLEARED AFTER DELETE')
    cache.delete('product_list')