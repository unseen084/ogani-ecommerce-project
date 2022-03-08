from django.urls import path, include
from . import views

app_name = "app"

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('blog/', include('blog.urls')),
]
