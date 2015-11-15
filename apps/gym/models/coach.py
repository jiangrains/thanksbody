#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin
    
class BaseCoach(models.Model):
    name = models.CharField(u"姓名", max_length=256)

    class Meta(object):
        abstract = False
        app_label = u"gym"
        verbose_name = u"BaseCoach"
        verbose_name_plural = u"BaseCoachs"


    def __init__(self, *args, **kwargs):
        super(BaseCoach, self).__init__(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
admin.site.register(BaseCoach)   