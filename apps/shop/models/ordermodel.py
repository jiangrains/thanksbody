# -*- coding: utf-8 -*-
from django.conf import settings
from util.loader import load_class


#==============================================================================
# Extensibility
#==============================================================================
# This overrides the various models with classes loaded from the corresponding
# setting if it exists.

# Order model
ORDER_MODEL = getattr(settings, 'SHOP_ORDER_MODEL',
    'shop.models.defaults.order.Order')
Order = load_class(ORDER_MODEL, 'SHOP_ORDER_MODEL')

# Order item model
ORDERITEM_MODEL = getattr(settings, 'SHOP_ORDERITEM_MODEL',
    'shop.models.defaults.orderitem.OrderItem')
OrderItem = load_class(ORDERITEM_MODEL, 'SHOP_ORDERITEM_MODEL')