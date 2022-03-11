from django.shortcuts import render, get_object_or_404

# Create your views here.
from shop.models import Product


def productinfo(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.filter(category=product.category).exclude(pk=product_id)
    return render(request, 'shop/shop-details.html', {'product': product, 'products': products})
