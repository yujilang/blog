from  django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import Input

from .models import Profile
from django.forms import ModelForm
#  第一种方法
from django.contrib.auth.models import User

#  第二种方法
#from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        #  设置表单显示字段
        fields = ['avatar']
        #  设置字段的标签名字
        labels = {'avatar':'头像'}

class User1Form(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class User2Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'phone' ,'avatar']
        labels = {'avatar': '用户头像',
                  'nickname':'昵称',
                  'phone':'手机号码'}
