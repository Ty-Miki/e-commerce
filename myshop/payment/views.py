from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from decimal import Decimal
import stripe

from orders.models import Order

# Create the stripe instances
stripe.api_key = settings.CREDENTIALS.get('STRIPE_SECRET_KEY')
stripe.api_version = settings.CREDENTIALS.get('STRIPE_API_VERSION')

def payment_process(request: HttpRequest) -> HttpResponse: 
    order_id = request.session.get(settings.ORDER_SESSION_ID, None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # Add order items to the stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    }
                },
                'quantity': item.quantity,
            })

        # Create stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        
        # redirect to stripe payment form
        return redirect(session.url, code=303)
    
    else:
        return render(request, 'payment/process.html', locals())
    

def payment_completed(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')