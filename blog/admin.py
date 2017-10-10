from django.contrib import admin
from .models import *

#  自定义后台显示
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']


#  在后台管理页面注册
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
# Register your models here.
