from django.db import models

from django.contrib.auth.models import User

#  第一种方法
class Profile(models.Model):
    #  给自定义的用户模型新增了一个 nickname（昵称）属性，
    #  用来记录用户的昵称信息
    nickname = models.CharField(max_length=64)

    #  Profile 与 User 是一对一的关系
    user = models.OneToOneField(User)

#  第二种方法
#  这种方法只能用于第一次迁移数据库之前设置
# from django.contrib.auth.models import AbstractUser
#
# class User(AbstractUser):
#     nickname = models.CharField(max_length=64,blank=True)
#
#     class Meta(AbstractUser.Meta):
#         pass

# Create your models here.
