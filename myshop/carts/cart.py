from decimal import Decimal
from django.conf import settings
from shop.models import Product
from django.http import HttpRequest

class Cart:
    def __init__(self, request: HttpRequest) -> None:
        '''Initialize the cart'''

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID]= {}
        self.cart = cart

    def save(self):
        # mark the session as modified to make sure it gets saved
        self.session.modified = True
    
    def add(self, product:Product, quantity: int = 1, override_quantity: bool = False) -> None:
        '''Add a product to cart or update its quantity'''

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
            
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def remove(self, product:Product) -> None:
        '''Remove a product from the cart'''
        
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''Iterate ovet the items in the cart and get the products from the DB'''

        product_ids = self.cart.keys()

        # get the product objects from DB and add them to cart.
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        # Iterate through the cart and yield a product item.
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self) -> int:
        '''count all the items in the cart'''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        '''remove cart from session'''
        del self.session[settings.CART_SESSION_ID]
        self.save()
    