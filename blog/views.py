from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title':'blog index',
        'welcome':'nice to meet you'
    }
    return render(request,'blog/index.html',context)
    #return HttpResponse('<h1>hello world<h1>')
# Create your views here.
