from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from blog.models import Blog
from shop.models import Product

from .forms import CustomerRegistrationForm, ProfileEditForm


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


def userProfile(request):
    #Have to change when db is made
    initial_data = {  # 1st Method
        'first_name': "request.user.email",
        'last_name': "request.user.last_name",
        'country': "dhgfdfrhh",
        'address': "fdhgffdh",
        'city': "hgfdhgf",
        'postal_code': "hggerhy",
        'phone_number': "gedhtfdh",
        'email': "gdgdfrhdh",
    }

    if request.method=='POST':
        form=ProfileEditForm(request.POST or None)
        if form.is_valid():
            form.save()
            #Some_TOdo_code_here
            return render(request, 'app/user_profile.html', {'form': form})
    else:
        form=ProfileEditForm(initial=initial_data)
        #redirect(Signup_teacher_r)
    return render(request, 'app/user_profile.html', {'form': form})


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
            login(request, obj)
            return redirect('app:home')
        return render(request, 'app/signup.html', {'form': form})





