from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('productinfo/<int:product_id>/', views.productinfo, name='productinfo'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),
]
