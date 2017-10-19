from django.shortcuts import render,redirect

from .forms import PostForm


def publishs(request):
    user = request.user
    if request.method == 'POST':
       form = PostForm(request.POST)

       if form.is_valid():
           post = form.save(commit=False)
           post.author = user
           post.save()
           #  将多对多关系数据保存到数据库
           form.save_m2m()
           return redirect('blog:index')

    else:
        form = PostForm()
        return render(request, 'publish/publishs.html', locals())
# Create your views here.
