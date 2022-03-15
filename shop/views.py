from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from shop.models import *


def productinfo(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.filter(category=product.category).exclude(pk=product_id)
    return render(request, 'shop/shop-details.html', {'product': product, 'products': products})


# will delete
def add_to_cart(request, product_id):
    pass
    # user = request.user
    # product = get_object_or_404(Product, pk=product_id)
    # Cart(user=user, product=product).save()
    # return redirect('shop:show_cart')


# will delete
def show_cart(request):
    pass
    # if request.user.is_authenticated:
    #     cart = Cart.objects.filter(user=request.user)
    #     amount = 0.0
    #     shipping_amount = 80.0
    #     total_amount = 0.0
    #     cart_product = list(cart)
    #     if cart_product:
    #         for p in cart_product:
    #             if p.product.discounted_price is not None:
    #                 tempamount = (p.quantity * p.product.discounted_price)
    #             else:
    #                 tempamount = (p.quantity * p.product.price)
    #             amount += tempamount
    #         total_amount = amount + shipping_amount
    #         return render(request, 'shop/shopping-cart.html', {'carts': cart,
    #                                                            'totalamount': total_amount,
    #                                                            'amount': amount})
    #     else:
    #         return render(request, 'app/emptycart.html')


# will delete
def plus_cart(request):
    pass
    # if request.method == 'GET':
    #     product_id = request.GET['product_id']
    #     c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
    #     c.quantity += 1
    #     c.save()
    #     amount = 0.0
    #     total_amount = 0.0
    #     shipping_amount = 80.0
    #     cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    #     for p in cart_product:
    #         if p.product.discounted_price is not None:
    #             tempamount = (p.quantity * p.product.discounted_price)
    #         else:
    #             tempamount = (p.quantity * p.product.price)
    #         amount += tempamount
    #     total_amount = amount + shipping_amount
    #
    #     data = {
    #         'quantity': c.quantity,
    #         'amount': amount,
    #         'totalamount': total_amount
    #     }
    #     return JsonResponse(data)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': (0, 70)}

    context = {'items': items, 'order': order}
    return render(request, 'shop/shopping-cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': (0, 70)}

    context = {'items': items, 'order': order}

    return render(request, 'shop/checkout.html', context)

