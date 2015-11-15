# -*- coding: utf-8 -*-
from shop.models_bases import BaseCartItem
from django.contrib import admin


class CartItem(BaseCartItem):
    class Meta(object):
        abstract = False
        app_label = u"shop"
        verbose_name = u"Cart item"
        verbose_name_plural = u"Cart items"
        
admin.site.register(CartItem)         