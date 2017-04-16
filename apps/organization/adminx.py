#_*_ coding: utf-8 _*_
__author__ = 'Frank'
__date__ = '2017/2/5 23:12'

import xadmin
from .models import City, CourseOrg, Teacher

class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    filter_list = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city']
    filter_list = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    # 当有一个外键指向course-org时，以ajax方式显示course-org供select
    # Todo 用了没效果
    relfield_style = 'fk_ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'woek_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'woek_position', 'points', 'click_nums', 'fav_nums']
    filter_list = ['org', 'name', 'work_years', 'work_company', 'woek_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)