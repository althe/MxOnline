#_*_ coding: utf-8 _*_
__author__ = 'Frank'
__date__ = '2017/2/5 21:18'

from .models import Course, Lesson, Video, courseResource
import xadmin

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    search_fieids = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']  # 可以在章节里面按课程名搜索


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class courseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'download', 'add_time']
    search_fields = ['course', 'name', 'download', 'download']
    list_filter = ['course', 'name', 'download', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(courseResource, courseResourceAdmin)
