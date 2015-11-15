# -*- coding: utf-8 -*-
from shop.models_bases import BaseOrderItem
from django.contrib import admin


class OrderItem(BaseOrderItem):

    class Meta(object):
        abstract = False
        app_label = u"shop"
        verbose_name = u"Order item"
        verbose_name_plural = u"Order items"

admin.site.register(OrderItem) 