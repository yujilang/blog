from django.conf.urls import url

from . import views

app_name = 'publish'
urlpatterns = [
    url(r'^publish/$', views.publishs, name='publishs'),
    url(r'^submit_post/$',views.submit_post,name='submit_post'),
]