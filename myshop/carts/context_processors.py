from .cart import Cart
from django.http import HttpRequest

def cart(request: HttpRequest):
    return {'cart': Cart(request=request)}