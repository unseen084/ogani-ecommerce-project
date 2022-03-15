from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('productinfo/<int:product_id>/', views.productinfo, name='productinfo'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    # path('cart/', views.show_cart, name='show_cart'),
    # path('pluscart/', views.plus_cart, name='plus_cart'),
]
