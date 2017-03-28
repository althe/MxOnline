# _*_ encoding: utf-8 _*_

"""
@athor: frank
@time: 2017/3/26 21:37
"""
from django.conf.urls import url
from .views import CourseListView, CourseDetailView


urlpatterns = [
    url(r'^course_list/$', CourseListView.as_view(), name="course_list"),

    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name="course_detail"),
]