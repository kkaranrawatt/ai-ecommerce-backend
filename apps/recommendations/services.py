from django.db.models import Count
from .models import UserProductInteraction

def get_recommended_products(product_id):
    interactions= (
        UserProductInteraction.objects.filter(product_id=product_id)
        .values('user')
    )
    user_ids=[item['user'] for item in interactions]

    recommended_products=(
        UserProductInteraction.objects.filter(user_id__in=user_ids)
        .exclude(product_id=product_id).values('product')
        .annotate(total=Count('product')).order_by('-total')
    )
    return recommended_products
