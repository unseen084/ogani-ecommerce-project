from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordResetForm, MySetPasswordForm

from django.contrib.auth.models import User

app_name = "app"

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('signup/', views.CustomerRegistrationView.as_view(), name='signup'),
    # path('login/', views.loginuser, name='loginuser'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
                                                         authentication_form=LoginForm), name='loginuser'),
    path('logout/', auth_views.LogoutView.as_view(next_page='app:loginuser'), name='logoutuser'),
    path('profile/', views.userprofile, name='userprofile'),
    path('category/<str:type>/', views.category, name='category'),
]
