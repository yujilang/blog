from django.conf.urls import url
from . import views

# regular expression >>> re(r) 正则表达式


#  告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间
app_name = 'blog'
urlpatterns = [
    #  调用类视图的 as_view() 方法,将类视图转换成函数视图
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(),name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$',views.TagView.as_view(),name='tag'),
    #url(r'^search/$',views.search,name='search'),
]