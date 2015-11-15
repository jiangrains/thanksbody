#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib import admin
from gym.models.wechat import Wechat
    
class User(models.Model): 
    GENDER_MAN = 10
    GENDER_WOMAN = 20
    
    GENDER_CODES = (
        (GENDER_MAN, u"男"),
        (GENDER_WOMAN, u"女"),
    )    
 
    name = models.CharField(u"姓名", max_length=256)
    gender = models.IntegerField(choices=GENDER_CODES, default=GENDER_MAN, verbose_name=u"性别")
    phonenum = models.CharField(u"手机号码", max_length=32) 
    #如果wechat为None，说明该用户尚未绑定微信 
    wechat = models.OneToOneField(Wechat, blank=True, null=True, verbose_name=u"微信号") 
    address = models.TextField(u"住址", max_length=512, blank=True)

    class Meta(object):
        abstract = False
        app_label = u"gym"
        verbose_name = u"User"
        verbose_name_plural = u"Users"


    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        
    def __unicode__(self):
        return self.name

    def bind_wechat(self, wechat_nick):
        if self.wechat is None:
            self.wechat = Wechat(wechat_nick)            
        else:
            self.wechat.nick = wechat_nick
    
    def unbind_wechat(self):
        self.wechat = None
    
    def update_base_info(self, name, phonenum, address):
        self.name = name
        self.phonenum = phonenum
        self.address = address
        
admin.site.register(User)
