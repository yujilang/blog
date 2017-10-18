from django.contrib import admin

from .models import *

#  将 Comment 表注册到 admin 后台
#  自定义显示 parent_comment text 字段
class CommentAdmin(admin.ModelAdmin):
    list_display = ['parent_comment', 'text']

admin.site.register(Comment, CommentAdmin)
# Register your models here.
