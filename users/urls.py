from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required
app_name = 'users'
urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^show/(?P<pk>[0-9]+)$', login_required(views.show), name='usershow')
]