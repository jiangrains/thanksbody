# -*- coding: utf-8 -*-
from shop.models_bases import BaseProduct
from shop.models_bases.managers import ProductManager
from django.contrib import admin


class Product(BaseProduct):
    objects = ProductManager()

    class Meta(object):
        abstract = False
        app_label = u"shop"
        verbose_name = u"Product"
        verbose_name_plural = u"Products"

admin.site.register(Product) 