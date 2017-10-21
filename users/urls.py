from django.conf.urls import url

from . import views
app_name = 'users'
urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^show/(?P<pk>[0-9]+)/$', views.show, name='usershow'),
    url(r'^change/(?P<pk>[0-9]+)/$', views.change, name='change'),
]