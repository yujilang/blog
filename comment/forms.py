from django import forms

from django.forms import Textarea

from .models import Comment

#  Django 的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类
class CommentForm(forms.ModelForm):
    #  表单的内部类 Meta
    class Meta:
        #  model = Comment 表明这个表单对应的数据库模型是 Comment 类
        model = Comment
        #  指定了表单需要显示的字段
        fields = {
            'text',
        }
        widgets = {'text': Textarea(attrs={'class': "form-control",
                                           'cols': 10,
                                           'rows': 3})}
