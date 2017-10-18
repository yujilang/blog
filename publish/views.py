from django.shortcuts import render,redirect
from django.http import HttpResponse

from blog.models import Category,Tag,Post

from django.contrib.auth.models import User

def publishs(request):
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    return render(request ,'publish/publishs.html', locals())

def submit_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        categorys = request.POST.get('category')
        category = Category.objects.get(name=categorys)
        # tag = request.POST.get('tag')
        # tags = Tag.objects.get(name=tag)
        body = request.POST.get('content')
        author = User.objects.get(username=request.user.username)
        Post.objects.create(title=title,category=category,body=body,author=author)
        return redirect('blog:index')
# Create your views here.
