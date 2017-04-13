# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', blank=True, default=True)  # 外键指向CourseOrg
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    teacher = models.ForeignKey(Teacher, verbose_name=u'课程讲师', null=True, blank=True)
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情', )
    degree = models.CharField(verbose_name=u'课程难度', choices=(('cj','初级'),('zj','中级'),('gj','高级')), max_length=2)
    category = models.CharField(max_length=20, verbose_name=u'课程类别', default=u'后端开发')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面图片')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    need_know = models.CharField(default='', max_length=300, verbose_name=u'课程须知')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name=u'能学到什么')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    # 获取课程章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    # 获取课程对应的章节信息
    def get_course_lesson(self):
        return self.lesson_set.all()

    # 拿到学习用户
    def get_learnUsers(self):
        return self.usercourse_set.all()[:5]

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    # 获取章节对应的视频信息
    def get_lesson_video(self):
        return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):   #视频信息
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, default='', verbose_name=u'访问地址')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class courseResource(models.Model):  #课程资源
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'课程资源', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name