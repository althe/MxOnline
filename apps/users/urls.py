# _*_ encoding: utf-8 _*_

"""
@athor: frank
@time: 2017/4/5 20:24
"""
# _*_ encoding:utf-8 _*_

from django.conf.urls import url, include
from users.views import UserCenterView, UploadImageView

urlpatterns = [

    # 用户信息页
    url(r'^info/$', UserCenterView.as_view(), name="info"),
    # 修改头像
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),

]

