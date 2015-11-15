#-*- encoding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from decimal import Decimal
from gym.models import User
from util.fields import CurrencyField
from util.loader import get_model_string



class BaseProduct(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Name")
    slug = models.SlugField(unique=True, verbose_name=u"Slug")
    active = models.BooleanField(default=False, verbose_name=u"Active")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=u"Date added")
    last_modified = models.DateTimeField(auto_now=True, verbose_name=u"Last modified")
    unit_price = CurrencyField(verbose_name=u"Unit price")

    class Meta(object):
        abstract = True
        app_label = u"shop"
        verbose_name = u"Product"
        verbose_name_plural = u"Products"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(u"product_detail", args=[self.slug]) 

    def get_price(self):
        """
        Returns the price for this item (provided for extensibility).
        """
        return self.unit_price

    def get_name(self):
        """
        Returns the name of this Product (provided for extensibility).
        """
        return self.name

    def get_product_reference(self):
        """
        Returns product reference of this Product (provided for extensibility).
        """
        return unicode(self.pk)

    @property
    def can_be_added_to_cart(self):
        return self.active        


        
class BaseCart(models.Model):
    """
    This should be a rather simple list of items. 
    
    Ideally it should be bound to a session and not to a User is we want to let 
    people buy from our shop without having to register with us.
    """
    # If the user is null, that means this is used for a session
    user = models.OneToOneField(User, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # items is the related_name of BaseCartItem
    
    class Meta(object):
        abstract = True
        app_label = u"shop"
        verbose_name = u"Cart"
        verbose_name_plural = u"Carts"

    def __init__(self, *args, **kwargs):
        super(BaseCart, self).__init__(*args, **kwargs)
        self.total_price = Decimal('0.0')
        self._updated_cart_items = None
        
    def add_product(self, product, quantity=1, queryset=None):
        from shop.models import CartItem
        
        # check if product can be added at all
        if not getattr(product, u"can_be_added_to_cart", True):
            return None
        
        # get the last updated timestamp
        # also saves cart object if it is not saved
        self.save()        
        
        if queryset is None:
            queryset = CartItem.objects.filter(cart=self, product=product)
        item = queryset
        
        if item.exists():
            cart_item = item[0]
            cart_item.quantity = cart_item.quantity + quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=self, quantity=quantity, product=product)
            cart_item.save()

        return cart_item

    def update_quantity(self, cart_item_id, quantity):
        cart_item = self.items.get(pk=cart_item_id)
        
        if quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        self.save()
        
        return cart_item
        
    def delete_item(self, cart_item_id):
        cart_item = self.items.get(pk=cart_item_id)
        cart_item.delete()
        self.save()
        
    def set_item_to_buy(self, cart_item_id):
        cart_item = self.items.get(pk=cart_item_id)
        cart_item.flag = cart_item.NEED_BUY_NOW
        cart_item.save()
        
    def set_item_not_to_buy(self, cart_item_id):
        cart_item = self.items.get(pk=cart_item_id)
        cart_item.flag = cart_item.STILL_IN_CART
        cart_item.save()   
        
    def empty(self):
        """
        Remove all cart items
        """
        if self.pk:
            self.items.all().delete()
            self.delete()
            
    @property
    def total_quantity(self):
        """
        Returns the total quantity of all items in the cart.
        """
        return sum([ci.quantity for ci in self.items.all()])

    @property
    def is_empty(self):
        return self.total_quantity == 0
        
    def get_updated_cart_items(self):
        """
        Returns updated cart items after update() has been called and
        cart modifiers have been processed for all cart items.
        """
        assert self._updated_cart_items is not None, ('Cart needs to be '
            'updated before calling get_updated_cart_items.')
        return self._updated_cart_items                
        
    def update(self, request):
        from shop.models import CartItem, Product
        
        items = CartItem.objects.filter(cart=self).order_by("pk")
        
        self.total_price = Decimal('0.0')
        
        for item in items:  # For each CartItem (order line)...
            self.total_price = self.total_price + item.update(request)
            
        # Cache updated cart items
        self._updated_cart_items = items                


class BaseCartItem(models.Model):
    """
    This is a holder for the quantity of items in the cart and, obviously, a
    pointer to the actual Product being purchased :)
    """
    NEED_BUY_NOW = 10  # The product should be delete and then move to order if the cart item is in this flag when user pays 
    STILL_IN_CART = 20  # The product will stiil in the cart    
    
    cart = models.ForeignKey(get_model_string(u"Cart"), related_name=u"items")
    quantity = models.IntegerField()
    product = models.ForeignKey(get_model_string(u"Product"))
    # whether need buy now
    flag = models.IntegerField()

    class Meta(object):
        abstract = True
        app_label = u"shop"
        verbose_name = u"Cart item"
        verbose_name_plural = u"Cart items"

    def __init__(self, *args, **kwargs):
        # That will hold extra fields to display to the user
        # (ex. taxes, discount)
        super(BaseCartItem, self).__init__(*args, **kwargs)
        self.flag = self.STILL_IN_CART
        self.line_total = Decimal('0.0')

    def update(self, request):
        self.line_total = self.product.get_price() * self.quantity
        
        return self.line_total
        


class BaseOrder(models.Model):
    PROCESSING = 10  # New order, addresses and shipping/payment methods chosen
    CONFIRMING = 20  # The order is pending confirmation (user is on the confirm view if has)
    CONFIRMED = 30  # The order was confirmed (user is in the payment backend)
    COMPLETED = 40  # Payment backend successfully completed (shipping if has)
    SHIPPED = 50  # The order was shipped to client(the order is done
    CANCELED = 60  # The order was canceled
    
        
    STATUS_CODES = (
        (PROCESSING, u"Processing"),
        (CONFIRMING, u"Confirming"),
        (CONFIRMED, u"Confirmed"),
        (COMPLETED, u"Completed"),
        (SHIPPED, u"Shipped"),
        (CANCELED, u"Canceled"),
    )    
    
    # If the user is null, the order was created with a session
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=u"顾客")
    status = models.IntegerField(choices=STATUS_CODES, default=PROCESSING, verbose_name=u"Status")
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"Create")
    modified = models.DateTimeField(auto_now=True, verbose_name=u"Updated")
    order_total = CurrencyField(verbose_name=u"Order Total")
    cart_pk = models.PositiveIntegerField(blank=True, null=True, verbose_name=u"Cart primary key")
    
    class Meta(object):
        abstract = True
        app_label = u"shop"
        verbose_name = u"Order"
        verbose_name_plural = u"Orders"
        
    def __unicode__(self):
        return u"Order ID: %(id)s" % {u"id": self.pk}        
        
    # when user has payed , the order is completed, so we can do the next step(ship or send to other system).    
    def is_completed(self):
        return (self.status == self.COMPLETED) or (self.status == self.SHIPPED)    


class BaseOrderItem(models.Model):
    order = models.ForeignKey(get_model_string(u"Order"), related_name=u"items", verbose_name=u"Order")
    product_reference = models.CharField(max_length=255, verbose_name=u"Product reference")
    product_name = models.CharField(max_length=255, blank=True, verbose_name=u"Product name")
    product = models.ForeignKey(get_model_string(u"Product"), null=True, blank=True, verbose_name=u"Product")
    unit_price = CurrencyField(verbose_name=u"Unit price")
    quantity = models.IntegerField(verbose_name=u"Quantity")

    class Meta(object):
        abstract = True
        app_label = u"shop"
        verbose_name = u"Order item"
        verbose_name_plural = u"Order items"    
