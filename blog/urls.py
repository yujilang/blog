from django.conf.urls import url
from . import views

# regular expression >>> re(r) 正则表达式


#  告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间
app_name = 'blog'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category'),
]