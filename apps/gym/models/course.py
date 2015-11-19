#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin
from shop.models.productmodel import Product
from gymnasium import Gymnasium
from coach import BaseCoach
    
class BaseCourse(Product):     
    COURSE_TYPE_GROUP = 10
    COURSE_TYPE_PRIVATE_TEACH = 20    
    COURSE_TYPE_COACH_ORDER = 30
    COURSE_TYPE_FREE_FITNESS = 40
    COURSE_TYPE = (
        (COURSE_TYPE_GROUP, u"团体课"),
        (COURSE_TYPE_PRIVATE_TEACH, u"私教课"),
        (COURSE_TYPE_COACH_ORDER, u"教练预约课程"),
        (COURSE_TYPE_FREE_FITNESS, u"自由健身"),        
    )


    COURSE_STATUS_SIGNUP = 10
    COURSE_STATUS_RUNNING = 20
    COURSE_STATUS_ENDED = 30
    COURSE_STATUS_CANCEL = 40
    COURSE_STATUS = (
        (COURSE_STATUS_SIGNUP, u"报名中"),
        (COURSE_STATUS_RUNNING, u"开课中"),
        (COURSE_STATUS_ENDED, u"已结束"),
        (COURSE_STATUS_CANCEL, u"已取消"),
    )    
    
    #name = models.CharField(u"课程名称", max_length=256)
    type = models.IntegerField(choices=COURSE_TYPE, default=COURSE_TYPE_LARGE_GROUP, verbose_name=u"课程类型")
    gymnasium = models.ForeignKey(Gymnasium, null=True, blank=True, verbose_name=u"场馆")
    coach = models.ForeignKey(BaseCoach, null=True, blank=True, verbose_name=u"教练")
    class_cnt = models.IntegerField(default=0, verbose_name=u"课程节数")
    min_user = models.IntegerField(default=1, verbose_name=u"最小开课人数")
    max_user = models.IntegerField(default=20, verbose_name=u"最大开课人数")
    user_cnt = models.IntegerField(default=0, verbose_name=u"实际报名人数")
    status = models.IntegerField(choces=COURSE_STATUS, default=COURSE_STATUS_SIGNUP, verbose_name=u"课程状态")

    class Meta(object):
        abstract = False
        app_label = u"gym"
        verbose_name = u"BaseCourse"
        verbose_name_plural = u"BaseCourses"


    def __init__(self, *args, **kwargs):
        super(BaseCourse, self).__init__(*args, **kwargs)
        self.status = COURSE_STATUS_SIGNUP
        self.user_cnt = 0
        
    def __unicode__(self):
        return self.name


class UserCourse(models.Model):
    user = models.ForeignKey(User, verbose_name=u"用户")
    course = models.ForeignKey(User, verbose_name=u"课程")
        
        
#所有的课表(class)        
class FitnessClass(models.Model):
    course = models.ForeignKey(BaseCourse, related_name=u"classes", verbose_name=u"课程")
    class_time = models.DateTimeField(auto_now=True, verbose_name=u"上课时间")
    gymnasium = models.ForeignKey(Gymnasium, verbose_name=u"上课场馆")
    room = models.IntegerField(default=0, verbose_name=u"上课房间")
    check_in_cnt = models.IntegerField(verbose_name=u"实际上课人数")
    
class CheckInItem(models.Model):
    user = models.ForeignKey(User, related_name=u"checkin_items", verbose_name=u"用户")
    fitnessclass = models.ForeignKey(FitnessClass, related_name=u"checkin_items", verbose_name=u"课程")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=u"签到时间")
    
    
admin.site.register(BaseCourse)    
