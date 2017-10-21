from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'publish'
urlpatterns = [
    url(r'^publish/$', login_required(views.publishs), name='publishs'),
    url(r'^change_post/(?P<pk>[0-9]+)/$',login_required(views.change_post),name='change_post'),
]