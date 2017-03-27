# _*_ encoding: utf-8 _*_

"""
@athor: frank
@time: 2017/3/26 21:37
"""
from django.conf.urls import url
from .views import CourseListView


urlpatterns = [
    url(r'^course_list/$', CourseListView.as_view(), name="course_list"),
]