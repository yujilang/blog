from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import *

from comment.forms import CommentForm

#  Markdown 是一种 HTML 文本标记语言，只要遵循它约定的语法格式，
#  Markdown 的渲染器就能够把我们写的文章转换为标准的 HTML 文档，
#  从而让我们的文章呈现更加丰富的格式，例如标题、列表、代码块等等 HTML 元素。
from markdown import markdown


#  文章总数页面视图函数
def index(request):
    #  获取Post的所有数据，并按最新的创建时间在上进行排序
    #  Post.objects.all()   查找所有数据
    #  order_by()  对数据进行排序
    post_list = Post.objects.all()

    #  页面渲染
    context = {
        'post_list':post_list,
    }
    return render(request,'blog/index.html',context)

#   文章详情页面视图函数
def detail(request,pk):
    #  根据pk主键在Post中查找数据，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
    #  get_object_or_404() 包含try：  except:
    post = get_object_or_404(Post,pk=pk)

    #  调用 increase_views() 方法，使得阅读量+1
    post.increase_views()

    #  对 post.body 多了一个中间步骤，先将 Markdown 格式的文本渲染成 HTML 文本再传递给模板
    #  参数 extensions，是对 Markdown 语法的拓展
    #  设置完成后，在发布的文章详情页没有看到预期的效果，而是类似于一堆乱码一样的 HTML 标签，
    #  因为 Django 出于安全方面的考虑，任何的 HTML 代码在 Django 的模板中都会被转义
    #  为了解除转义，只需在模板标签使用 safe 过滤器即可，即
    #  在模板中找到展示博客文章主体的 {{ post.body }} 部分，为其加上 safe 过滤器，{{ post.body|safe }}
    post.body = markdown(post.body,extensions=[
                         'markdown.extensions.extra',  #  extra 本身包含很多拓展
                        'markdown.extensions.codehilite',  #  codehilite 是语法高亮拓展
                        'markdown.extensions.toc',  #  toc 允许我们自动生成目录
                        ])

    #  在顶部导入 CommentForm，这里实例化没有 request.POST 作为参数，因此表单都是空的
    form = CommentForm()

    #  获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    #  将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {
        'post':post,
        'form':form,
        'comment_list':comment_list,
    }
    return  render(request,'blog/detail.html',context)

#  归档页面
def archives(request,year,month):
    #  使用 objects.filter() 方法过滤文章
    #  created_time 是 Python 的 date 对象，其有一个 year 和 month 属性
    #  Python 中类实例调用属性的方法通常是 created_time.year，
    #  但是由于这里作为函数的参数列表，所以 Django 要求我们把点替换成了两个下划线，
    #  即 created_time__year。
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    context = {
        'post_list':post_list
    }
    return render(request,'blog/index.html',context)

#  分类页面
def category(request,pk):
    #  根据分类的 pk 值（也就是被访问的分类的 id 值） 在 Category 中获取这个分类的信息（分类的name）
    cate = get_object_or_404(Category,pk=pk)
    #  根据 cate 在 Post 中过滤出该分类下的所有文章，并进行排序
    post_list = Post.objects.filter(category=cate)
    context = {
        'post_list':post_list
    }
    return render(request,'blog/index.html',context)
# Create your views here.
