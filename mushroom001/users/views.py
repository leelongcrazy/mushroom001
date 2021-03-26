from django.contrib.auth import logout as dj_logout, authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View


from .forms import LoginForm, SignupForm
from .models import UserInfo


# 主页
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html', {})


# 注册页面
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        if request.user.is_authenticated:
            message = ['warning', "您已经成功登录，如需注册请先退出！"]
        return render(request, 'signup.html', locals())

    def post(self, request):
        register_form = SignupForm(request.POST)
        message = ['warning', '表单信息无效，请重新输入注册']
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            work_id = register_form.cleaned_data.get('work_id')
            # gender = register_form.cleaned_data.get('gender')
            if password1 != password2:
                message = ['warning', "两次密码输入不一致！！！"]
                return render(request, 'signup.html', locals())
            if UserInfo.objects.filter(username=username):
                message = ['warning', "该用户名已经被注册了！！！"]
                return render(request, 'signup.html', locals())
            if UserInfo.objects.filter(work_id=work_id):
                message = ['warning', "该工号已经被注册了！！！"]
                return render(request, 'signup.html', locals())
            if UserInfo.objects.filter(email=email):
                message = ['warning', "该邮箱已经被注册了！！！"]
                return render(request, 'signup.html', locals())

            newUser = UserInfo()
            newUser.username = username
            newUser.email = email
            newUser.password = make_password(password1)
            newUser.work_id = work_id
            newUser.save()
            message = ['primary', "您已经注册成功，请登录..."]
            return render(request, 'login.html', locals())
        else:
            return render(request, 'signup.html', locals())


# 登录界面
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        # message = []
        if login_form.is_valid():
            user_name = login_form.cleaned_data.get('username')
            pass_word = login_form.cleaned_data.get('password')
            user = authenticate(username=user_name, password=pass_word)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
                # return HttpResponseRedirect(request.POST.get('redirect_to', reverse('index')))
                # return HttpResponse(request.POST.get('redirect_to'))
            else:
                message = ['warning', "请注意检查用户名或密码是否有错误..."]
                return render(request, 'login.html', locals())
        else:
            message =['warning', "请重新登录！！！"]
            return render(request, 'login.html', locals())


# 登出界面
class LogoutView(View):
    def get(self, request):
        # login_form = LoginForm()
        message = ["success", "登出成功，返回主页..."]
        request.session.flush()
        return render(request, 'index.html', locals())
        # return HttpResponseRedirect(reverse('index'), locals())
