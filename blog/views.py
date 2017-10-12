from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import *

from comment.forms import CommentForm

#  Markdown 是一种 HTML 文本标记语言，只要遵循它约定的语法格式，
#  Markdown 的渲染器就能够把我们写的文章转换为标准的 HTML 文档，
#  从而让我们的文章呈现更加丰富的格式，例如标题、列表、代码块等等 HTML 元素。
from markdown import markdown

#  generic 通用视图
#  针对从数据库中获取某个模型列表数据，使用 ListView 类视图
#  查看某篇文章的详情，就是从数据库中获取这篇文章的记录然后渲染模板
#  对于这种类型的需求，Django 提供了一个 DetailView 类视图
from django.views.generic import ListView,DetailView

#  文章总数页面视图函数

# def index(request):
#     #  获取Post的所有数据，并按最新的创建时间在上进行排序
#     #  Post.objects.all()   查找所有数据
#     #  order_by()  对数据进行排序
#     post_list = Post.objects.all()
#
#     #  页面渲染
#     context = {
#         'post_list':post_list,
#     }
#     return render(request,'blog/index.html',context)

#  将 index 视图函数改造成类视图
class IndexView(ListView):
    #  将 model 指定为 Post，告诉 Django 我要获取的模型是 Post
    model = Post
    #  指定这个视图渲染的模板
    template_name = 'blog/index.html'
    #  指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。
    context_object_name = 'post_list'
    #  指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 2

#   文章详情页面视图函数

# def detail(request,pk):
#     #  根据pk主键在Post中查找数据，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
#     #  get_object_or_404() 包含try：  except:
#     post = get_object_or_404(Post,pk=pk)
#
#     #  调用 increase_views() 方法，使得阅读量+1
#     post.increase_views()
#
#     #  对 post.body 多了一个中间步骤，先将 Markdown 格式的文本渲染成 HTML 文本再传递给模板
#     #  参数 extensions，是对 Markdown 语法的拓展
#     #  设置完成后，在发布的文章详情页没有看到预期的效果，而是类似于一堆乱码一样的 HTML 标签，
#     #  因为 Django 出于安全方面的考虑，任何的 HTML 代码在 Django 的模板中都会被转义
#     #  为了解除转义，只需在模板标签使用 safe 过滤器即可，即
#     #  在模板中找到展示博客文章主体的 {{ post.body }} 部分，为其加上 safe 过滤器，{{ post.body|safe }}
#     post.body = markdown(post.body,extensions=[
#                          'markdown.extensions.extra',  #  extra 本身包含很多拓展
#                         'markdown.extensions.codehilite',  #  codehilite 是语法高亮拓展
#                         'markdown.extensions.toc',  #  toc 允许我们自动生成目录
#                         ])
#
#     #  在顶部导入 CommentForm，这里实例化没有 request.POST 作为参数，因此表单都是空的
#     form = CommentForm()
#
#     #  获取这篇 post 下的全部评论
#     comment_list = post.comment_set.all()
#
#     #  将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
#     context = {
#         'post':post,
#         'form':form,
#         'comment_list':comment_list,
#     }
#     return  render(request,'blog/detail.html',context)

#  将 detail 视图函数改造成类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    #  覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
    #  get 方法返回的是一个 HttpResponse 实例
    def get(self, request, *args, **kwargs):

        #  之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        #  才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super().get(request,*args,**kwargs)

        #  将文章阅读量 +1
        #  self.object 的值就是被访问的文章 post
        #  每次请求文章详情页，都会调用get方法，因此increase_views写在get()当中比较合适
        self.object.increase_views()

        #  视图必须返回一个 HttpResponse 对象
        return response

    #  覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        post.body = markdown(post.body, extensions=[
            'markdown.extensions.extra',  # extra 本身包含很多拓展
            'markdown.extensions.codehilite',  # codehilite 是语法高亮拓展
            'markdown.extensions.toc',  # toc 允许我们自动生成目录
        ])
        return post

    #  覆写 get_context_data 的目的是因为除了将 post 传递给模板外
    #  还要把评论表单、 post 下的评论列表传递给模板。 也就是往 context 里添加内容
    def get_context_data(self, **kwargs):

        #  把 post 加入到 context 中
        context = super().get_context_data(**kwargs)

        #  空表单
        form = CommentForm()

        #  全部评论
        #  self.object 等价于 post
        comment_list = self.object.comment_set.all()

        #  context 已有 post，所以使用 update 更新 context
        context.update({
            'form':form,
            'comment_list':comment_list,
        })
        return context
#  归档页面
# def archives(request,year,month):
#     #  使用 objects.filter() 方法过滤文章
#     #  created_time 是 Python 的 date 对象，其有一个 year 和 month 属性
#     #  Python 中类实例调用属性的方法通常是 created_time.year，
#     #  但是由于这里作为函数的参数列表，所以 Django 要求我们把点替换成了两个下划线，
#     #  即 created_time__year。
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     )
#     context = {
#         'post_list':post_list
#     }
#     return render(request,'blog/index.html',context)

#  将 archives 视图函数改造成类视图
#  可以直接继承 IndexView
class ArchivesView(IndexView):
    #  覆写了父类的 get_queryset 方法。
    #  该方法默认获取指定模型的全部列表数据
    def get_queryset(self):
        return super().get_queryset().filter(
            #  在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，
            #  非命名组参数值保存在实例的 args 属性（是一个列表）里
            #  这里使用 self.kwargs.get() 来获取从 URL 捕获的参数值
            created_time__year=self.kwargs.get('year'),
            created_time__month=self.kwargs.get('month'),
        )

#  分类页面
# def category(request,pk):
#     #  根据分类的 pk 值（也就是被访问的分类的 id 值） 在 Category 中获取这个分类的信息（分类的name）
#     cate = get_object_or_404(Category,pk=pk)
#     #  根据 cate 在 Post 中过滤出该分类下的所有文章，并进行排序
#     post_list = Post.objects.filter(category=cate)
#     context = {
#         'post_list':post_list
#     }
#     return render(request,'blog/index.html',context)

#  将 category 视图函数改造成类视图
class CategoryView(IndexView):
    def get_queryset(self):
        #  根据从 URL 中捕获的分类 pk（也就是 id）获取分类
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        #  调用父类的 get_queryset 方法获得全部文章列表，
        #  对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回
        #  下面 filter(category=cate) 中的 category 是 post.category
        return super().get_queryset().filter(category=cate)
# Create your views here.
