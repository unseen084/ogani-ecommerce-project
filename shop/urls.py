from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('productinfo/<int:product_id>/', views.productinfo, name='productinfo'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateitem, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),

]
