from django.db import transaction
from .models import Order, OrderItem
from apps.products.models import Product

@transaction.atomic
def create_order(user, items_data):
    total_price= 0
    order= Order.objects.create(user=user)

    for item in items_data:
        product = Product.objects.select_for_update().get(
            id=item['product_id']
        )
        quantity= item['quantity']

        if product.stock < quantity:
            raise Exception(
                f"Insufficient stock for {product.name}"
            )
        
        #reduce stock
        product.stock -= quantity
        product.save()

        item_total= product.price * quantity

        total_price += item_total

        OrderItem.objects.create(
            order= order,
            product= product,
            quantity= quantity,
            price= product.price
        )

    order.total_price = total_price
    order.save()
    return order

