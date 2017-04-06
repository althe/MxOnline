#_*_ coding: utf-8 _*_
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View

from forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_util import LoginRequiredMixin
from .models import UserProfile, EmailVerifyRecord
import json


class ResetView(View):  # 处理修改密码链接
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "pwd_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request): # 处理用户提交业务逻辑
        # 首先实例化form表单对象
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "pwd_reset.html", {"email":email, "msg": "两次密码不一致，请重新输入"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "pwd_reset.html", {"email":email, "modify_form": modify_form})


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form": forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forgetpwd_form": forget_form, "msg": "请重新输入验证码"})


class ActiveUserView(View):     #邮箱验证码激活
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code = active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                # form需要回传是因为需要用到验证码功能
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已存在！"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "邮箱未激活！"})
            else:
                return render(request, "login.html", {"msg": "账号或者密码错误！"}) # 检查输入之后是否错误！
        else:
            return render(request, "login.html", {"login_form": login_form}) # 检查是否输入错误


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserCenterView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter_info.html', {})


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        imageForm = UploadImageForm(request.POST, request.FILES, instance=request.user)
        res = {}
        if imageForm.is_valid():
            imageForm.save()
            res['status'] = 'success'
            res['msg'] = '头像修改成功！'
        else:
            res['status'] = 'fail'
            res['msg'] = '头像修改失败！'
        return HttpResponse(json.dumps(res), content_type='application/json')


class UpdatePwdView(View):
    def post(self, request):

        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg": "两次密码不一致，请重新输入"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success", "msg": "修改密码成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')
