# _*_ encoding:utf-8 _*_

from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin
from users.views import LoginView, RegisterView, ActiveUserView, ForgetView, ResetView, ModifyPwdView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
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

]

