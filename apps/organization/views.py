# _*_ encoding:utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import City, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from organization.forms import UserAskForm
from operation.models import UserFavorite


class OrgView(View):
    def get(self, request):
        all_citys = City.objects.all()
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()  # 城市数量
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 对城市结果集进行筛选
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)


        # 页面展示排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 6, request=request)
        orgs = p.page(page)
        return render(request, "org_list.html", {'all_citys': all_citys,
                                                 'all_orgs': orgs,
                                                 'org_nums': org_nums,
                                                 'city_id': city_id,
                                                 'category': category,
                                                 'hot_orgs': hot_orgs,
                                                 'sort': sort,
                                                 })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit = True)
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type="application/json")


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id = int(org_id))
        ## 判断是否收藏逻辑
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]  # 外键可以反向拿到对应的值
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org_detail_homepage.html', {'course_org':course_org,
                                                            'all_courses':all_courses,
                                                            'all_teachers':all_teachers,
                                                            'current_page': current_page,
                                                            'has_fav': has_fav})


class OrgCourseView(View):
    '''
    课程首页
    '''
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id = int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]  # 外键可以反向拿到对应的值

        return render(request, 'org_detail_course.html', {'course_org':course_org,
                                                            'all_courses':all_courses,
                                                            'current_page': current_page,
                                                            'has_fav': has_fav})


class OrgDescView(View):
    '''
    机构介绍
    '''
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id = int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org_detail_desc.html', {'course_org':course_org,
                                                          'current_page': current_page,
                                                        'has_fav': has_fav})


class OrgTeacherView(View):
    '''
    机构教师s首页
    '''
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id = int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()

        return render(request, 'org_detail_teacher.html', {'course_org':course_org,
                                                            'all_teachers':all_teachers,
                                                          'current_page': current_page,
                                                           'has_fav': has_fav})


class AddFavView(View):
    '''
    用户收藏,以及取消收藏
    '''
    def post(self, request):
        # 用户收藏之前，先拿到收藏页面类别，和id
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 先判断用户是否登陆
        if not request.user.is_authenticated():
            # 如果没登陆，则直接返回登陆界面
            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type="application/json")
        # 去数据库查询是否存在收藏记录
        exit_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exit_records:
            # 如果已经存在，则表示用户想取消收藏
            exit_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
        else:
            fav_user = UserFavorite()
            if  int(fav_id) > 0 and int(fav_type) > 0:
                fav_user.user = request.user
                fav_user.fav_type = int(fav_type)
                fav_user.fav_id = int(fav_id)
                fav_user.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                pass
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


