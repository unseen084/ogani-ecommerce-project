from django.urls import path, include
from . import views

app_name = "app"

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('signup/', views.signup, name='signup'),
]
