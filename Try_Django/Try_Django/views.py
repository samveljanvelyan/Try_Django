from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from blog.models import BlogPost


def home_page(request):
    my_title = 'Hello there ....'
    qs = BlogPost.objects.all()[:5]
    context = {'title': 'Welcome to Try Django', 'blog_list': qs}
    return render(request, "home.html", context)


def about_page(request):
    return render(request, "about.html", {"title": 'About Us'})


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    context = {
        'title': 'Contact us', 'form': form
    }
    return render(request, "form.html", context)
