#  创建自定义模板标签

from django import template

#  导入所有模型
from ..models import *

from django.db.models.aggregates import Count

#  首先创建一个全局register变量，用来注册自定义标签和过滤器
#  实例化 template.Library() 类
register = template.Library()

#  将函数装饰为 register.simple_tag

#  最新文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]

#  归档
@register.simple_tag
def archives():
    #  dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，
    #  且是 Python 的 date 对象，精确到月份，降序排列。
    #  created_time ，即 Post 的创建时间，month 是精度
    #  order='DESC' 表明降序排列（即离当前越近的时间越排在前面）
    return Post.objects.dates('created_time','month',order='DESC')

#  分类
@register.simple_tag
def get_categories():
    #  Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    #  annotate 的作用就是往模型类中新增一个属性，
    #  这里新增了 num_posts 属性，注意并非保存到数据库，
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

#  标签云
@register.simple_tag
def get_tags():
    # 与分类同理
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)