from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import *

#  Markdown 是一种 HTML 文本标记语言，只要遵循它约定的语法格式，
#  Markdown 的渲染器就能够把我们写的文章转换为标准的 HTML 文档，
#  从而让我们的文章呈现更加丰富的格式，例如标题、列表、代码块等等 HTML 元素。
from markdown import markdown


#  文章总数页面视图函数
def index(request):
    #  获取Post的所有数据，并按最新的创建时间在上进行排序
    #  Post.objects.all()   查找所有数据
    #  order_by()  对数据进行排序
    post_list = Post.objects.all().order_by('-created_time')

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


    context = {'post':post}
    return  render(request,'blog/detail.html',context)
# Create your views here.
