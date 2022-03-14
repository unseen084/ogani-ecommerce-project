from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from shop.models import Product, Cart


def productinfo(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.filter(category=product.category).exclude(pk=product_id)
    return render(request, 'shop/shop-details.html', {'product': product, 'products': products})


def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    Cart(user=user, product=product).save()
    return redirect('shop:show_cart')


def show_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'shop/shopping-cart.html', {'carts': cart})

