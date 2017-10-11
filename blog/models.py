from django.db import models
from django.urls import reverse
# User是一个自带的模型类，里面是用户的字段
from django.contrib.auth.models import User

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
    created_time=models.DateTimeField()
    #  修改时间
    modified_time=models.DateTimeField()
    #  摘要 可以为空
    exerpt=models.CharField(max_length=256,blank=True)

    #  关系
    #  文章和分类是多对一的关系
    category = models.ForeignKey(Category)
    #  文章和标签是多对多的关系 文章可以没有标签blank=True
    tags = models.ManyToManyField(Tag, blank=True)
    #  文章和作者是多对一的关系，其中作者从django.contrib.auth.models导入的User模型类
    author = models.ForeignKey(User)


    #  自定义 get_absolute_url 方法
    #  从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        #  使用reverse函数，生成一个完整的url
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

    class Meta:
        #  ordering 属性用来指定文章排序方式，
        #  这样指定以后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序，
        #  因此可以删掉视图函数中对文章列表中返回结果进行排序的代码了。
        ordering = ['-created_time','-modified_time']