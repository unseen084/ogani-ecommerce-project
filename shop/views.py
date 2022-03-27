import datetime
import json

from django.core.mail.backends import console
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from shop.models import *
from . import utils
from .utils import *


def productinfo(request, product_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': (0, 70)}
        cartItems = 0

    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.filter(category=product.category).exclude(pk=product_id)

    context = {'order': order, 'cartItems': cartItems, 'product': product, 'products': products}
    return render(request, 'shop/shop-details.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/shopping-cart.html', context)


def checkout(request):
    print('Checkout...')
    data = cartData(request, in_check_out=True)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    customer = data['customer']
    shipping_address = data['shipping_address']
    context = {'items': items, 'order': order, 'shipping_address': shipping_address,
               'customer': customer, 'cartItems': cartItems}

    return render(request, 'shop/checkout.html', context)


def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ', action, 'Product: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = orderitem.quantity + 1
    elif action == 'remove':
        orderitem.quantity = orderitem.quantity - 1
    orderitem.save()

    if orderitem.quantity == 0:
        orderitem.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    print('process order start...')
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('Data: ', data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print('user not logged in')
        customer, order = guestOrder(request, data)
        print('Customer: ',customer,' order: ', order)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total[1]:
        order.complete = True
    order.save()
    print('process order end...')
    return JsonResponse('payment complete', safe=False)
