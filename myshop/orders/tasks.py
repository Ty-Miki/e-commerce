from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    """Task to send an email notification when users order."""

    order = Order.objects.get(id=order_id)
    subject = f'Order number {order.id}'
    message = f'Dear {order.first_name},\n\n' \
            f'You have successfully placed an order.' \
            f'Your order ID is {order.id}'
    mail_sent = send_mail(subject,
                          message,
                          "ethioadvance@gmail.com",
                          [order.email])
    
    return mail_sent


