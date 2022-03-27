import json

import shop
from shop.models import *


def cookieCart(request):
    print('CookieCart...')
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': (0, 70)}
    cartItems = 0
    tupleval1 = 0
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            if product.discounted_price is not None:
                total = (product.discounted_price * cart[i]["quantity"])
            else:
                total = (product.price * cart[i]["quantity"])

            tupleval1 += total
            item = {
                'product': {
                    'id': product.id,
                    'title': product.title,
                    'price': product.price,
                    'discounted_price': product.discounted_price,
                    'image1': product.image1,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)
        except Exception as e:
            print('err: ', e)
    tupleval2 = order['get_cart_total'][1] + tupleval1
    order['get_cart_total'] = (tupleval1, tupleval2)
    print('CookieCart end!')
    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request, in_check_out=False):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        shipping_address = ShippingAddress.objects.get(customer_id=customer.id, order_id=None)

    else:
        print('user not auth\'ed -> CartData')
        shipping_address = []
        customer = []
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    if in_check_out:
        context['shipping_address'] = shipping_address
        context['customer'] = customer
    return context


def guestOrder(request, data):
    print('guest order start...')
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    try:
        customer = Customer.objects.filter(email=email)[0]
    except Exception as e:
        print('customer error: ', e)
        customer = Customer.objects.create(
            email=email,
            name=name
        )
        customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        country=data['shipping']['country'],
        postal_code=data['shipping']['postal_code'],
        phone_number=data['shipping']['phone_number']
    )
    print('guest order end...')
    return customer, order
