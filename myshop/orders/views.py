from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from .models import OrderItem
from .forms import OrderCreateForm
from carts.cart import Cart
from django.http import HttpRequest, HttpResponse
from .tasks import order_created

def order_create(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Clear the cart
            cart.clear()

            # launch asynchronous task to send emails
            order_created.delay(order.id)


            # set the order in the session
            request.session[settings.ORDER_SESSION_ID] = order.id

            # Redirect for payment
            return redirect(reverse('payment:process'))
    
    else:
        form = OrderCreateForm()
    
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
                      
    