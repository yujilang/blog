from django.conf.urls import url
from . import views

# regular expression >>> re(r) 正则表达式

urlpatterns = [
    url(r'^$',views.index,name='index'),
]