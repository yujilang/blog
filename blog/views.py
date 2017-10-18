from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import *

from comment.forms import CommentForm

#  Markdown 是一种 HTML 文本标记语言，只要遵循它约定的语法格式，
#  Markdown 的渲染器就能够把我们写的文章转换为标准的 HTML 文档，
#  从而让我们的文章呈现更加丰富的格式，例如标题、列表、代码块等等 HTML 元素。
from markdown import markdown,Markdown

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

#  generic 通用视图
#  针对从数据库中获取某个模型列表数据，使用 ListView 类视图
#  查看某篇文章的详情，就是从数据库中获取这篇文章的记录然后渲染模板
#  对于这种类型的需求，Django 提供了一个 DetailView 类视图
from django.views.generic import ListView,DetailView

from django.db.models import Q

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

    def pagination_data(self, paginator, page, is_paginated):
        #  如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
        if not is_paginated:
            return {}

        #  设置默认值
        #  1，当前页左边连续的页码号，初始值为空
        left = []
        #  2，当前页右边连续的页码号，初始值为空
        right = []
        #  3，表示第 1 页页码后是否需要显示省略号
        left_has_more = False
        #  4，表示最后一页页码前是否需要显示省略号
        right_has_more = False
        #  5，表示是否需要显示第 1 页的页码号
        #  因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，
        #  此时就无需再显示第 1 页的页码号
        #  其它情况下第一页的页码是始终需要显示的。
        #  初始值为 False
        first = False
        #  6，表示是否需要显示最后一页的页码号。
        #  需要此指示变量的理由和上面相同。
        last = False
        #  7，获得用户当前请求的页码号
        page_number = page.number

        #  获得分页后的总页数
        total_pages = paginator.num_pages
        #  获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        #  判断当前页码

        #  如果当前页是第一页
        if page_number == 1:
            #  如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            #  此时只要获取当前页右边的连续页码号，
            #  比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            #  注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。 切片时如果溢出自动截断
            right = page_range[page_number:page_number + 2]
            #  如果最右边的页码号比最后一页的页码号减去 1 还要小，
            #  说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True
            #  如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            #  所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        #  如果当前页是最后一页
        elif page_number == total_pages:
            #  如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            #  此时只要获取当前页左边的连续页码号。
            #  比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            #  这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            #  如果最左边的页码号比第 2 页页码号还大，
            #  说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True
            #  如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            #  所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True

        #  如果当前页是中间的某一页
        else:
            #  用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            #  这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            #  是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            #  是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        #  设置返回值
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

    """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
    """
    def get_context_data(self, **kwargs):
        #  首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        #  父类生成的字典中已有 paginator、 page_obj、 is_paginated 这三个模板变量，
        #  paginator 是 Paginator 的一个实例，
        #  page_obj 是 Page 的一个实例，
        #  is_paginated 是一个布尔变量，用于指示是否已分页。
        #  例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时is_paginated=False。

        #  由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        #  调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        #  将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        #  将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        #  注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context


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

        #  先实例化了一个 Markdown 类 md，和 markdown() 方法一样
        md = Markdown(extensions=[
            'markdown.extensions.extra',  # extra 本身包含很多拓展
            'markdown.extensions.codehilite',  # codehilite 是语法高亮拓展
            #  在顶部引入 TocExtension 和 slugify
            #  使用了 django.utils.text 中的 slugify 方法，该方法可以很好地处理中文
            #  把锚点修改为文章的实际标题
            TocExtension(slugify=slugify),
        ])

        #  使用该实例的 convert 方法将 post.body 中的Markdown 文本渲染成 HTML 文本
        post.body = md.convert(post.body)

        #  把 md.toc 的值赋给 post.toc 属性
        #  要注意这个 post 实例本身是没有 md 属性的，
        #  我们给它动态添加了md 属性，这就是 Python 动态语言的好处

        post.toc = md.toc
        return post

    #  覆写 get_context_data 的目的是因为除了将 post 传递给模板外
    #  还要把评论表单、 post 下的评论列表传递给模板。 也就是往 context 里添加内容
    def get_context_data(self, **kwargs):

        #  把 post 加入到 context 中
        context = super().get_context_data(**kwargs)

        #  空表单
        form = CommentForm()

        #  context 已有 post，所以使用 update 更新 context
        context.update({
            'form':form,
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

#  标签云页面
#  原理同上
class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)

def search(request):
    #  用户通过表单 get 方法提交的数据 Django 为我们保存在 request.GET 里,
    #  类似于 Python 字典的对象
    #  使用 get 方法从字典里取出键 q 对应的值，即用户的搜索关键词
    q = request.GET.get('q')
    error_msg = ''

    #  如果用户没有输入搜索关键词而提交了表单，就无需执行查询，
    #  在模板中渲染一个错误提示信息
    if not q:
        error_msg = '请输入关键词'
        context = {'error_msg':error_msg}
        return render(request,'blog/index.html',context)

    #  title__icontains=q，即 title 中包含（contains）关键字 q
    #  body__icontains=q, 即 body 中包含（contains）关键字 q
    #  Q(title__icontains=q) | Q(body__icontains=q) 表示标题（title）含有关键词 q 或者正文（body）含有关键词 q
    #  或逻辑使用 | 符号
    post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))

    context = {
        'post_list':post_list,
        'error_msg': error_msg,
    }
    return render(request,'blog/index.html',context)
# Create your views here.
