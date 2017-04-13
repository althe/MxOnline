# _*_ encoding:utf-8 _*_

from django.conf.urls import url, include
from django.views.static import serve
import xadmin
from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetView, ResetView, ModifyPwdView
from MxOnline.settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="active"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^forget/$', ForgetView.as_view(), name="forget_pwd"),
    url(r'^modify/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构首页
    url(r'^org/', include('organization.urls', namespace="org")), # 命名空间用于区分
    # 课程详情首页
    url(r'^course/', include('courses.urls', namespace="course")),
    # 用户信息首页
    url(r'^users/', include('users.urls', namespace="users")),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}), # 机构logo路径配置
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}), # 机构logo路径配置
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
