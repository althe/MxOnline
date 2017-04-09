# _*_ encoding: utf-8 _*_
"""
@athor: frank
@time: 2017/4/5 20:24
"""

from django.conf.urls import url, include
from users.views import UserCenterView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView

urlpatterns = [

    # 用户信息页
    url(r'^info/$', UserCenterView.as_view(), name="info"),
    # 修改头像
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    # 用户中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 发送更新邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    # 更新邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    # 用户收藏课程
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

]

