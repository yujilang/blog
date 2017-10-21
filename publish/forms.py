from django.forms import ModelForm, Textarea, Select
from django.forms.widgets import Input
from django import forms
from blog.models import Post,Category,Tag

class PostForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.order_by('id'),
        label="标签",
        help_text="可以多选 按住 ”Control“，或者Mac上的 “Command”，可以选择多个。",
        widget=forms.SelectMultiple(
            attrs={
                'multiple':'',
                'class': 'form-control',
                'style': 'width:100%'
            }
        ),
    )
    class Meta:
        model = Post
        fields = ['title','category','tags','body']
        widgets = {'title': Input(attrs={'class':"form-control"}),
                   'category': Select(attrs={'class':'form-control'}),
                   'body': Textarea(attrs={'class': "form-control",'rows':8})}
        labels = {'title': '标题',
                  'category': '分类',
                  'body': '内容'}

