#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin
    
class Gymnasium(models.Model):
    name = models.CharField(u"场馆名", max_length=256)

    class Meta(object):
        abstract = False
        app_label = u"gym"
        verbose_name = u"Gymnasium"
        verbose_name_plural = u"Gymnasiums"


    def __init__(self, *args, **kwargs):
        super(Gymnasium, self).__init__(*args, **kwargs)
        
    def __unicode__(self):
        return self.name
    
admin.site.register(Gymnasium)   