from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import *


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
    context = {'post':post}
    return  render(request,'blog/detail.html',context)
# Create your views here.
