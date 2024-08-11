from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Category, Product

# Create your views here.
def product_list(request: HttpRequest, 
                 category_slug: str | None = None) -> HttpResponse:

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(avaliable=True)

    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)
    
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request: HttpRequest, id: int, slug: str) -> HttpResponse:

    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                avaliable=True)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product})