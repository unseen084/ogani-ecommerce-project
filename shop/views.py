import datetime
import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from shop.models import *


def productinfo(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.filter(category=product.category).exclude(pk=product_id)
    return render(request, 'shop/shop-details.html', {'product': product, 'products': products})


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': (0, 70)}
        cartItems = 0

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/shopping-cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        shipping_address = ShippingAddress.objects.get(customer_id=customer.id, order_id=None)

    else:
        items = []
        order = {'get_cart_total': (0, 70)}

    context = {'items': items, 'order': order, 'shipping_address': shipping_address,
               'customer': customer}

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
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total[1]:
            order.complete = True
        order.save()

        # ship
        # ShippingAddress.objects.create(
        #     customer=customer,
        #     order=order,
        #     address=data['shipping']['address'],
        #     city=data['shipping']['city'],
        #     country=data['shipping']['country'],
        #     postal_code=data['shipping']['postal_code'],
        #     phone_number=data['shipping']['phone_number'],
        # )

    else:
        print('user not logged in')
    print('data: ', request.body)
    return JsonResponse('payment complete', safe=False)
