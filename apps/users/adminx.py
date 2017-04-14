#_*_ coding: utf-8 _*_
__author__ = 'Frank'
__date__ = '2017/1/30 21:34'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from users.models import EmailVerifyRecord, Banner, UserProfile

# class UserProfileAdmin(UserAdmin):  # 自定义自己的user管理模块
#     pass


class BaseSetting(object): # 主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "哲商科技"
    site_footer = "哲商网络"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time'] # 显示字段
    search_fields = ['code', 'email', 'send_type']             # 搜索关键字段
    list_filter = ['code', 'email', 'send_type', 'send_time']  #筛选字段


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# from django.contrib.auth.models import User
# xadmin.site.unregister(User)   # 卸载xadmin自带user管理模块
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin) # 注册自己的user管理模块