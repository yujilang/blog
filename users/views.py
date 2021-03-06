from django.shortcuts import render, redirect
from .forms import *
from .models import Profile
from django.contrib.auth.models import User

#  带表单的视图函数的经典写法
def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value = "{{ next }}" / >
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    #  只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':

        #  request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        #  这里提交的就是用户名（username）、密码（password）、邮箱（email）
        #  用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)
        #  上传文件要加入 request.FILES 字段
        form1 = ProfileForm(request.POST, request.FILES)
        #  验证数据的合法性
        if form.is_valid():
            if form1.is_valid():
                #  如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库（所谓的注册，就是把用户信息放在数据库中）
                user = form.save()
                profile = form1.save(commit=False)
                profile.user = user
                profile.save()

                #  注册成功，跳转回首页
                if redirect_to:
                    return redirect(redirect_to)
                else:
                    return redirect('login')
    else:
        #  请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()
        form1 = ProfileForm()

    #  渲染模板
    #  如果用户正在访问注册页面，则渲染的是一个空的注册表单

    #  如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'profile':form1,'next':redirect_to})

#  用户信息显示视图函数
def show(request,pk):
    user_list = User.objects.get(id=int(pk))
    return render(request, 'users/show.html', locals())

#  用户信息修改视图函数
def change(request, pk):
    #   获取当前 id 对象的用户信息
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        #   将用户所修改信息与获取信息相关联，指定给谁做修改
        user_form = User1Form(request.POST, instance=user)
        profile_form = User2Form(request.POST, request.FILES, instance=profile)
        if user_form.is_valid():
            if profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('users:usershow',pk)
    else:
        #  将当前 id 信息返回给页面
        user_form = User1Form( instance=user)
        profile_form = User2Form( instance=profile)
    return render(request, 'users/change.html', locals())