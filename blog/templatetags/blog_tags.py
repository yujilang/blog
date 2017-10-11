#  创建自定义模板标签

from django import template

#  导入所有模型
from ..models import *

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
    return Category.objects.all()