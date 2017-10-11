from django.db import models



class Comment(models.Model):
    #  评论人的名字
    name = models.CharField(max_length=128)
    #  邮箱
    email = models.EmailField(max_length=256)
    #  网址
    url = models.URLField(blank=True)
    #  评论内容
    text = models.TextField()
    #  评论时间
    #  auto_now_add 的作用是，当评论数据保存到数据库时，
    #  自动把 created_time 的值指定为当前时间
    created_time = models.DateTimeField(auto_now_add=True)
    #  评论与文章是多对一的关系
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]


