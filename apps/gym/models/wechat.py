#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin

class Wechat(models.Model): 
    nick = models.CharField(u"微信号", max_length=256)
    openId = models.CharField(u"OpenID", max_length=256, blank=True)
    
    class Meta(object):
        abstract = False
        app_label = u"gym"
        verbose_name = u"Wechat"
        verbose_name_plural = u"Wechats"

    def __init__(self, *args, **kwargs):
        super(Wechat, self).__init__(*args, **kwargs)
        
    def __unicode__(self):
        return self.nick
    
admin.site.register(Wechat)    