from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('productinfo/<int:product_id>/', views.productinfo, name='productinfo'),
]
