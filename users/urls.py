from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
app_name = 'users'
urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^show/(?P<pk>[0-9]+)/$', login_required(views.show), name='usershow'),
    url(r'^change/(?P<pk>[0-9]+)/$', login_required(views.change), name='change'),
]