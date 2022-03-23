from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from blog.models import Blog
from shop.models import Product, Customer, ShippingAddress, CATEGORY_CHOICES

from .forms import CustomerRegistrationForm, ProfileEditForm


def home(request):
    blogs = Blog.objects.all()
    image_list = {}
    for item in CATEGORY_CHOICES:
        product = Product.objects.filter(category=item[0])
        if len(product) != 0:
            image_list[item[1]] = product[0].image1.url
        else:
            # default category image
            image_list[item[1]] = 'static/app/img/categories/cat-1.jpg'
    return render(request, 'app/index.html', {'blogs': blogs, 'img_list': image_list})


def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blog.html', {'blogs': blogs})


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop/shop-grid.html', {'products': products})


def contact(request):
    return render(request, 'app/contact.html')


def prepareInitialData(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user_id=request.user.id)
    shipping_address = ShippingAddress.objects.get(customer_id=customer.id, order_id=None)

    initial_data = {  # 1st Method
        'first_name': user.first_name,
        'last_name': user.last_name,
        'country': shipping_address.country,
        'address': shipping_address.address,
        'city': shipping_address.city,
        'postal_code': shipping_address.postal_code,
        'phone_number': shipping_address.phone_number,
        'email': request.user.email,
    }
    return initial_data


def userprofile(request):
    if request.method=='POST':
        form = ProfileEditForm(request.POST or None)
        if form.is_valid():
            User.objects.filter(id=request.user.id).update(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            Customer.objects.filter(user=request.user).update(email=form.cleaned_data['email'],
                                                              name=form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name'])
            customer = Customer.objects.filter(user=request.user)
            customer = customer[0]

            ShippingAddress.objects.filter(
                customer=customer).update(
                address=form.cleaned_data['address'],
                country=form.cleaned_data['country'],
                city = form.cleaned_data['city'],
                postal_code = form.cleaned_data['postal_code'],
                phone_number = form.cleaned_data['phone_number']
            )
            initial_data = prepareInitialData(request)
            form = ProfileEditForm(initial=initial_data)
            return render(request, 'app/user_profile.html', {'form': form})
    else:
        initial_data = prepareInitialData(request)
        form = ProfileEditForm(initial=initial_data)
        # redirect(Signup_teacher_r)
        return render(request, 'app/user_profile.html', {'form': form})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/signup.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        c = Customer()
        if form.is_valid():
            obj = form.save()
            obj.user = request.user
            obj.save()

            c.user = User.objects.get(id=obj.id)
            c.email = form.cleaned_data['email']
            c.name = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
            c.save()

            shipping = ShippingAddress()
            shipping.customer = c
            shipping.address = form.cleaned_data['address']
            shipping.country = form.cleaned_data['country']
            shipping.city = form.cleaned_data['city']
            shipping.postal_code = form.cleaned_data['postal_code']
            shipping.phone_number = form.cleaned_data['phone_number']
            shipping.save()

            login(request, obj)
            return redirect('app:home')
        return render(request, 'app/signup.html', {'form': form})
