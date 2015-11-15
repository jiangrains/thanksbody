# -*- coding: utf-8 -*-
from shop.models_bases import BaseOrder
from shop.models_bases.managers import OrderManager
from django.contrib import admin


class Order(BaseOrder):
    objects = OrderManager()

    class Meta(object):
        abstract = False
        app_label = u"shop"
        verbose_name = u"Order"
        verbose_name_plural = u"Orders"

admin.site.register(Order) 