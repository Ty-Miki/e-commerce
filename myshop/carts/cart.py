from decimal import Decimal
from django.conf import settings
from shop.models import Product
from django.http import HttpRequest

class Cart:
    def __init__(self, request: HttpRequest) -> None:
        "Initialize the cart"

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID]= {}
        self.cart = cart