from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderLineItem, OrderType


@receiver(post_save, sender=OrderLineItem)
def update_order_total(sender, instance, created, **kwargs):
    '''
    Update order total each time a line item is added,
    accounting for delivery costs and order discounts.
    '''
    order = instance.order_number
    order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    '''
    Update order total each time a line item is deleted,
    accounting for delivery costs and order discounts.
    '''
    order = instance.order_number
    order.update_total()
