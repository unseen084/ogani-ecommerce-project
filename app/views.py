from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from blog.models import Blog
from shop.models import Product

from .forms import CustomerRegistrationForm


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'app/index.html', {'blogs': blogs})


def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blog.html', {'blogs': blogs})


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop/shop-grid.html', {'products': products})


def contact(request):
    return render(request, 'app/contact.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/signup.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.user = request.user
            obj.save()
            return redirect('app:home')
        return render(request, 'app/signup.html', {'form': form})





