from celery import shared_task
import time

@shared_task
def send_order_confirmation_email(order_id):
    print(f"Sending confirmation email for Order {order_id}")

    time.sleep(5)
    print(f"Order {order_id} confirmed")
    return f"Done for order {order_id}"