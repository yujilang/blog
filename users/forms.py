from  django.contrib.auth.forms import UserCreationForm

#  第一种方法
from django.contrib.auth.models import User

#  第二种方法
#from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email']