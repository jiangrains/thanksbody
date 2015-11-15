# -*- coding: utf-8 -*-
from shop.models_bases import BaseCart
from django.contrib import admin


class Cart(BaseCart):
    class Meta(object):
        abstract = False
        app_label = u"shop"
        verbose_name = u"Cart"
        verbose_name_plural = u"Carts"
        
admin.site.register(Cart)        