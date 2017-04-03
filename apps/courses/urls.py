# _*_ encoding: utf-8 _*_

"""
@athor: frank
@time: 2017/3/26 21:37
"""
from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentView, AddCommentView


urlpatterns = [
    url(r'^course_list/$', CourseListView.as_view(), name="course_list"),

    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name="course_detail"),

    # 课程信息页
    url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name="course_info"),

    # 课程评论页
    url(r'^comment/(?P<course_id>\d+)$', CommentView.as_view(), name="course_comment"),

    # 提交评论
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
]