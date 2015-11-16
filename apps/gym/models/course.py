#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin
from shop.models.productmodel import Product
from gymnasium import Gymnasium
from coach import BaseCoach
    
class BaseCourse(Product):     
    COURSE_TYPE_LARGE_GROUP = 10
    COURSE_TYPE_MIDDLE_GROUP = 20
    COURSE_TYPE_SMALL_GROUP = 30
    COURSE_TYPE_PRIVATE_TEACH = 40
    COURSE_TYPE_FREE_FITNESS = 50
    
    COURSE_TYPE = (
        (COURSE_TYPE_LARGE_GROUP, u"大团体课"),
        (COURSE_TYPE_SMALL_GROUP, u"小团体课"),
        (COURSE_TYPE_PRIVATE_TEACH, u"私教课"),
    ) 
    #name = models.CharField(u"课程名称", max_length=256)
    type = models.IntegerField(choices=COURSE_TYPE, default=COURSE_TYPE_LARGE_GROUP, verbose_name=u"课程类型")
    gymnasium = models.OneToOneField(Gymnasium, null=True, blank=True, verbose_name=u"场馆")
    coach = models.OneToOneField(BaseCoach, null=True, blank=True, verbose_name=u"教练")
    min_person = models.IntegerField(verbose_name=u"最小开课人数", default=1)
    max_person = models.IntegerField(verbose_name=u"最大开课人数", default=20)

    class Meta(object):
        abstract = False
        app_label = u"gym"
        verbose_name = u"BaseCourse"
        verbose_name_plural = u"BaseCourses"


    def __init__(self, *args, **kwargs):
        super(BaseCourse, self).__init__(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
admin.site.register(BaseCourse)    
