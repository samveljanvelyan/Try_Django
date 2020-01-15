from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogPostModelForm
from .models import BlogPost


# Create your views here.


def blog_post_list_view(request):
    # List out objects
    qs = BlogPost.objects.all().published()  # queryset -> list of python object
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = 'list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)


@staff_member_required
def blog_post_create_view(request):
    # Create objects
    if not request.user.is_authenticated:
        return render(request, 'not-a-user.html', {})
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    # 1 object -> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'detail.html'
    context = {"object": obj}
    return render(request, template_name, context)


def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {'form': form, 'title': f'Update {obj.title}'}
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect('/blog')
    context = {'object': obj}
    return render(request, template_name, context)
