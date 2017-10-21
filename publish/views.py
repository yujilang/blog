from django.shortcuts import render,redirect

from blog.models import Post
from .forms import PostForm

#  发表文章视图函数
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

#  修改文章视图函数
def change_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'publish/change_post.html', {'form':form,'post_id':pk})
# Create your views here.
