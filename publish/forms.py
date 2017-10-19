from django.forms import ModelForm, Textarea
from django.forms.widgets import Input

from blog.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','category','tags','body']
        widgets = {'title': Input(attrs={'class':"form-control"}),
                   # 'tags': Input(attrs={'type': "checkbox"}),
                   # 'category': Input(attrs={'type': "radio"}),
                   'body': Textarea(attrs={'class': "form-control",'rows':8})}

