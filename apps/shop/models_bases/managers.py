# -*- coding: utf-8 -*-
from django.db import models
from util.compat.db import atomic


class ProductManager(models.Manager):
    """
    A more classic manager for Product filtering and manipulation.
    """
    def active(self):
        return self.filter(active=True)



class OrderManager(models.Manager):
    
    def get_unconfirmed_for_cart(self, cart):
        return self.filter(cart_pk=cart.pk, status__lt=self.model.CONFIRMED)
    
    def remove_old_orders(self, cart):
        old_olders = self.get_unconfirmed_for_cart(cart)
        old_orders.delete()
    
    def create_order_object(self, cart, request):
        """
        Create an empty order object and fill it with the given cart data.
        """
        order = self.model()
        order.cart_pk = cart.pk
        order.user = cart.user
        order.status = self.model.PROCESSING  # Processing
        order.order_total = cart.total_price
        return order
    
    @atomic
    def create_from_cart(self, cart, request): 
        from shop.models.cartmodel import CartItem
        # First, let's remove old orders(becase the network may send more than one request to us with a unique cart)
        self.remove_old_orders(cart)
        
        order = self.create_order_object(cart, request)
        order.save()
        
        # There, now move on to the order items.
        cart_items = CartItem.objects.filter(cart=cart, flag=CartItem.NEED_BUY_NOW)
        for item in cart_items:
            order_item = OrderItem()
            order_item.order = order
            order_item.product = item.product
            order_item.unit_price = item.product.get_price()            
            order_item.quantity = item.quantity
            order_item.product_reference = item.product.get_product_reference()
            order_item.product_name = item.product.get_name()
            order_item.save()
            item.delete()
  
        processing.send(self.model, order=order, cart=cart)
        return order
            
