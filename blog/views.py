from django.shortcuts import render, get_object_or_404
from .models import Blog

# Create your views here.


def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/blog-details.html', {'blog': blog})
