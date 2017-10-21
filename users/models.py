from django.core.validators import RegexValidator
from django.db import models

from django.contrib.auth.models import User

#  第一种方法
class Profile(models.Model):
    #  给自定义的用户模型新增了一个 nickname（昵称）属性，
    #  用来记录用户的昵称信息
    nickname = models.CharField(max_length=64)
    #  电话 可以为空
    phone = models.CharField(max_length=11, null=True, blank=True,
                             error_messages={
                                 'phone_err': '手机号码格式有误',
                             },
                             validators=[
                                 RegexValidator(regex='1[3578][0-9]{9}', message='手机号码格式有误',
                                                code='phone_err')])
    #  头像 upload_to 头像保存地址 default 默认头像
    avatar = models.ImageField(upload_to='avatar',default="avatar/1.jpg")

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
