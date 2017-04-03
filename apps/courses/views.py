# _*_ encoding:utf-8 _*_

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite, CourseComments, UserCourse
from .models import Course, courseResource
from utils.mixin_util import LoginRequiredMixin


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


class CourseDetailView(View):
    def get(self, request, course_id): # 此处接收的 course_id 是url里面配置的正则接收参过来的
        # course = request.POST.get(id= int(course_id))   注意：此处拿到课程id之后应该去数据库拿课程对象
        course = Course.objects.get(id=int(course_id))
        # user_course = Course.get_studyUsers()       获取学习用户 为什么不写在view里面

        # 统计课程点击数
        course.click_nums += 1
        course.save()

        # 收藏处理逻辑
        has_course_fav = False
        has_org_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_course_fav = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_org_fav = True

        return render(request, 'course_detail.html', {"course": course,
                                                      'has_course_fav': has_course_fav,
                                                      'has_org_fav': has_org_fav})


class CourseInfoView(LoginRequiredMixin, View):
    '''
    课程详情
    '''
    def get(self, request, course_id):
        # 返回单个课程详情
        course = Course.objects.get(id=int(course_id))
        # 返回学过当前课程的同学还学过哪些其他课程
        # 原理就是先拿到学过当前课程的所有学员id，然后拿到这些学员所学所有课程id,然后返回这些课程点击量最大的5个用来推荐
        user_courses = UserCourse.objects.filter(course=course)
        all_students_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=all_students_ids) # 用户查看课程对象
        # 推荐逻辑有待完善
        all_user_courses_id = [all_course.course.id for all_course in all_user_courses]
        relate_courses = Course.objects.filter(course_org_id__in=all_user_courses_id).order_by('-click_nums')[:5] # 相关用户看过的其他课程对象
        all_resource = courseResource.objects.filter(course=course)
        return render(request, 'course_video.html', {'course': course,
                                                     'relate_courses': relate_courses,
                                                     'all_resource': all_resource})


class CommentView(View):
    '''
    课程评论
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        comments = CourseComments.objects.all()
        all_resource = courseResource.objects.filter(course=course)
        return render(request, 'course_comment.html', {'course': course,
                                                     'comments': comments,
                                                     'all_resource': all_resource})

class AddCommentView(View): # 此处为什么不写进一个类？因为响应的不是同一个URL？
    '''
    添加评论
    '''
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type="application/json")

        # 添加评论当然先要拿到课程id,和评论内容
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        # 接下来就应该判断id是否合法，并实例化评论对象，并存入数据库
        if course_id >0 and comments:
            courseComments = CourseComments()
            courseComments.course = Course.objects.get(id=int(course_id))
            courseComments.comments = comments
            courseComments.user = request.user
            courseComments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"fail":"success", "msg":"评论失败"}', content_type="application/json")


