from django.db import models
from django.urls import reverse

# User是一个自带的模型类，里面是用户的字段
from django.contrib.auth.models import User

#  使用第二种方法时
#  使用 users 应用下的 User 用户模型
#from users.models import User

from markdown import Markdown
from django.utils.html import strip_tags
# Create your models here.

#  分类
class Category(models.Model):
    name=models.CharField(max_length=64)

    #  在后台选择显示的字段
    def __str__(self):
        return self.name

#  标签
class Tag(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return self.name

#  文章
class Post(models.Model):
    #  文章标题
    title=models.CharField(max_length=64)
    #  文章正文
    body=models.TextField()
    #  创建时间
    created_time=models.DateTimeField(auto_now_add=True)
    #  修改时间
    modified_time=models.DateTimeField(auto_now=True)
    #  摘要 可以为空
    exerpt=models.CharField(max_length=256,blank=True)

    #  关系
    #  文章和分类是多对一的关系
    category = models.ForeignKey(Category)
    #  文章和标签是多对多的关系 文章默认标签为 python
    tags = models.ManyToManyField(Tag, default='python')
    #  文章和作者是多对一的关系，其中作者从django.contrib.auth.models导入的User模型类
    author = models.ForeignKey(User)

    #  文章阅读量
    #  views 字段的类型为 PositiveIntegerField，该类型的值只允许为正整数或 0
    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views+=1
        #  调用 save 方法将更改后的值保存到数据库
        #  使用 update_fields 参数来告诉 Django 只更新数据库中 views 字段的值，以提高效率
        self.save(update_fields=['views'])

    #  自定义 get_absolute_url 方法
    #  从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        #  使用reverse函数，生成一个完整的url
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    #  复写 save（）方法,自动生成文章摘要
    def save(self, *args, **kwargs):
        #  如果没有填写摘要
        if not self.exerpt:
            #  首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            #  先将 Markdown 文本渲染成 HTML 文本
            #  strip_tags 去掉 HTML 文本的全部 HTML 标签
            #  从文本摘取前 32 个字符赋给 excerpt
            self.exerpt = strip_tags(md.convert(self.body))[:32]

        #  调用父类的 save 方法将数据保存到数据库中
        super().save(*args,**kwargs)

    class Meta:
        #  ordering 属性用来指定文章排序方式，
        #  这样指定以后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序，
        #  因此可以删掉视图函数中对文章列表中返回结果进行排序的代码了。
        ordering = ['-created_time','-modified_time']