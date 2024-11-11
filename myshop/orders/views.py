from django.shortcuts import render
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


        return render(request,
                      'orders/order/created.html',
                      {'order': order})
    
    else:
        form = OrderCreateForm()
    
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
                      
    