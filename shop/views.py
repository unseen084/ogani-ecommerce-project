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
        amount = 0.0
        shipping_amount = 80.0
        total_amount = 0.0
        cart_product = list(cart)
        print(cart_product)
        if cart_product:
            for p in cart_product:
                print(p.quantity, "*", p.product.discounted_price)
                if p.product.discounted_price is not None:
                    tempamount = (p.quantity * p.product.discounted_price)
                else:
                    tempamount = (p.quantity * p.product.price)
                amount += tempamount
            total_amount = amount + shipping_amount
        return render(request, 'shop/shopping-cart.html', {'carts': cart,
                                                           'totalamount': total_amount,
                                                           'amount': amount})

