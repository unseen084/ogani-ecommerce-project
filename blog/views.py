from django.shortcuts import render, get_object_or_404

from shop.models import Order
from .models import Blog

# Create your views here.


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems = 0

    context = {'blog': blog, 'cartItems': cartItems}
    return render(request, 'blog/blog-details.html', context)
