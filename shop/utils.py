import json
from shop.models import *


def cookieCart(request):
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
        except:
            pass
    tupleval2 = order['get_cart_total'][1] + tupleval1
    order['get_cart_total'] = (tupleval1, tupleval2)

    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request, in_check_out=False):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        shipping_address = ShippingAddress.objects.get(customer_id=customer.id, order_id=None)

    else:
        print('user not auth\'ed')
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
