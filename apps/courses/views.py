# _*_ encoding:utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course


class CourseListView(View):
    def get(self, request):
        org_courses = Course.objects.all().order_by('-add_time') # 默认按添加时间排序

        # 热门课程
        hot_courses = org_courses.order_by('-click_nums')[:3]

        # 页面内容排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                org_courses = org_courses.order_by('-students')
            elif sort == 'hot':
                org_courses = org_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_courses, 3, request=request)
        courses = p.page(page)

        return render(request, "course_list.html", {'all_courses': courses,
                                                    'sort': sort,
                                                    'hot_courses': hot_courses})