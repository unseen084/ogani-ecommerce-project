from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Blog
from shop.models import Product


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'app/index.html', {'blogs': blogs})


def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blog.html', {'blogs': blogs})


def contact(request):
    return render(request, 'app/contact.html')


def signup(request):
    return render(request, 'app/signup.html')


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop/shop-grid.html', {'products': products})


