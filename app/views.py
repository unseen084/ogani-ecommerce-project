from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from blog.models import Blog
from shop.models import Product, Customer, ShippingAddress, CATEGORY_CHOICES, Order, FEATURED_CATEGORY_CHOICES, CATEGORY_CHOICES_MAP
from shop.utils import *

from .forms import CustomerRegistrationForm, ProfileEditForm


def home(request):
    blogs = Blog.objects.all()

    # show cart item count
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    # category items
    image_list = get_category_items()
    # latest n items in 2D list
    latest_N_Products = get_N_latest_items()
    # Favourite n items in 2D list
    favourite_N_Products = get_N_favourite_items()
    # Featured n  items
    featured_N_products = get_N_featured_items()
    context = {'order': order, 'cartItems': cartItems,
               'blogs': blogs, 'img_list': image_list,
               'latest_N_Products': latest_N_Products,
               'favourite_N_Products': favourite_N_Products,
               'featured_N_products': featured_N_products}
    return render(request, 'app/index.html', context)


def category(request, type):
    products = Product.objects.filter(category=CATEGORY_CHOICES_MAP[type])
    # latest n items in 2D list
    latest_N_Products = get_N_latest_items()
    return render(request, 'app/searched-category.html', {'products': products, 'latest_N_Products': latest_N_Products})

def blog(request):
    blogs = Blog.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': (0, 70)}
        cartItems = 0

    context = {'order': order, 'cartItems': cartItems, 'blogs': blogs}

    return render(request, 'blog/blog.html', context)


def shop(request):
    products = Product.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    # latest n items in 2D list
    latest_N_Products = get_N_latest_items()

    context = {'order': order, 'cartItems': cartItems, 'products': products, 'latest_N_Products': latest_N_Products}

    return render(request, 'shop/shop-grid.html', context)


def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems = 0

    context = {'cartItems': cartItems}
    return render(request, 'app/contact.html', context)


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

# Helper functions

def get_N_featured_items():
    featured_N_products = []
    for item in FEATURED_CATEGORY_CHOICES:
        products = Product.objects.filter(category=item[0])
        if len(products) != 0:
            for product in products:
                featured_N_products.append({
                    'title': product.title,
                    'image': product.image1.url,
                    'price': product.price,
                    'category': item[1]
                })
    return featured_N_products

def get_N_favourite_items():
    favourite_products = Product.objects.all().order_by('-fav_count')[:9]
    favourite_N_Products = []
    n_prod = []
    for idx, prod in enumerate(favourite_products):
        n_prod.append({
            'title': prod.title,
            'image': prod.image1.url,
            'price': prod.price,
        })
        if (idx + 1) % 3 == 0:
            favourite_N_Products.append(n_prod)
            n_prod = []
    return favourite_N_Products

def get_N_latest_items():
    latest_products = Product.objects.all().order_by('-latest')[:9]
    latest_N_Products = []
    n_prod = []
    for idx, prod in enumerate(latest_products):
        n_prod.append({
            'title': prod.title,
            'image': prod.image1.url,
            'price': prod.price,
        })
        if (idx + 1) % 3 == 0:
            latest_N_Products.append(n_prod)
            n_prod = []
    return latest_N_Products

def get_category_items():
    image_list = {}
    for item in CATEGORY_CHOICES:
        product = Product.objects.filter(category=item[0])
        if len(product) != 0:
            image_list[item[1]] = product[0].image1.url
        else:
            # default category image
            image_list[item[1]] = 'static/app/img/categories/cat-1.jpg'
    return image_list


def search(request):
    print('Search...')
    query = request.GET['query']
    print(query)
    products = Product.objects.filter(Q(title__icontains=query))
    # latest n items in 2D list
    latest_N_Products = get_N_latest_items()
    return render(request, 'app/searched-category.html', {'products': products, 'latest_N_Products': latest_N_Products})

