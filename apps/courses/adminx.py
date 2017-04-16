#_*_ coding: utf-8 _*_
__author__ = 'Frank'
__date__ = '2017/2/5 21:18'

from .models import Course, BannerCourse, Lesson, Video, courseResource
import xadmin
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInLine(object):
    model = courseResource
    extra = 0


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    search_fieids = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    ordering = ['-click_nums'] # 指定课程管理后台页面排序规则
    readonly_fields = ['click_nums']  # 指定只读字段
    exclude = ['fav_nums']  # 指定不可见字段
    inlines = [LessonInline, CourseResourceInLine]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class CourseAdmin(object):                                                                      # python对于变量和方法其实是一样的
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'get_zj_nums', 'go_to', 'add_time']
    search_fieids = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    ordering = ['-click_nums'] # 指定课程管理后台页面排序规则
    list_editable = ['desc', 'degree']  # 指定可直接编辑字段  好东西
    refresh_times = [3, 5]     # 指定页面自动刷新时间
    readonly_fields = ['click_nums']  # 指定只读字段
    exclude = ['fav_nums']  # 指定不可见字段
    inlines = [LessonInline, CourseResourceInLine]  # 课程管理中关联 章节 和 课程资源模块
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):  # 这里是一个接口
        obj = self.new_obj
        obj.save() # 此处先保存，避免漏计数
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(courseResource, courseResourceAdmin)
