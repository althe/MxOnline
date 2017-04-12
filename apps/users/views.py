#_*_ coding: utf-8 _*_
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View

from forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UpdateUserInfoForm
from utils.email_send import send_register_email
from utils.mixin_util import LoginRequiredMixin
from .models import UserProfile, EmailVerifyRecord
import json
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course
from organization.models import CourseOrg, Teacher


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


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))



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

    def post(self, request):
        userInfoForm = UpdateUserInfoForm(request.POST, instance=request.user)# 指明当前用户，否则会新建一个用户
        if userInfoForm.is_valid():
            userInfoForm.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(userInfoForm.errors), content_type='application/json')


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


class UpdatePwdView(LoginRequiredMixin, View):
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
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        # 首先拿到新输入的邮箱，并去数据库查询是否重复
        # 如果不是重复的，则向该邮箱发送验证码
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已存在！"}', content_type='application/json')

        send_register_email(email, "update_email")
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        '''
        思路：拿到对应的邮箱地址和发送的验证码，并去数据库检查是否有对应的记录
        如果有，则对用用户进行update操作，如果没有则返回出错消息，前端就会显示错误。
        '''
        Email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        exist_code = EmailVerifyRecord.objects.filter(email=Email, code=code)
        if exist_code:
            user = request.user
            user.email = Email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter_mycourse.html', {'user_courses': user_courses})


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        FavCourses = []
        favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav in favs:
            course_id = fav.fav_id
            course = Course.objects.get(id = course_id)
            FavCourses.append(course)
        return render(request, 'usercenter_fav_course.html', {'FavCourses': FavCourses})


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        FavOrgs = []
        favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav in favs:
            org_id = fav.fav_id
            org = CourseOrg.objects.get(id=org_id)
            FavOrgs.append(org)
        return render(request, 'usercenter_fav_org.html', {'FavOrgs': FavOrgs})


class myFavteacherView(LoginRequiredMixin, View):
    def get(self, request):
        FavTeachers = []
        favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav in favs:
            teacher_id = fav.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            FavTeachers.append(teacher)
        return render(request, 'usercenter_fav_teacher.html', {'FavTeachers': FavTeachers})


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        mymessages = UserMessage.objects.filter(user=request.user.id)
        for message in mymessages:
            message.has_read = True
            message.save()
        return render(request, 'usercenter_usermessage.html', {'mymessages': mymessages})