import enum
from django.db.models import Sum
import uuid
from django.conf import settings
from django.db import models

from products.models import Product
from profiles.models import UserProfile

# Create your models here.


class OrderType(enum.Enum):
    DELIVERY = "Delivery"
    PICKUP = "Pickup"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    order_type = models.CharField(max_length=20, choices=OrderType.choices(),
                                  default=OrderType.PICKUP)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=10, null=True, blank=False)
    # limit delivery in just a country since this is food delivery
    country = models.CharField(
        max_length=40, null=False, blank=False, default='Norway')
    delivery_charge = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    order_discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    expected_done_date = models.DateField(null=True, blank=False)
    expected_done_time = models.TimeField(null=True, blank=False)
    order_note = models.TextField(max_length=500, null=True, blank=True)
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        '''
        Generate a random, unique order number using UUID
        '''
        return uuid.uuid4().hex.upper()

    def update_total(self):
        '''
        Update grand total each time a line item is added,
        accounting for delivery costs and order discounts.
        '''
        self.order_total = self.lineitems.aggregate(Sum('order_item_total'))[
            'order_item_total__sum'] or 0

        if self.order_total >= settings.ORDER_DISCOUNT_THRESHOLD:
            self.order_discount = self.order_total * \
                settings.ORDER_DISCOUNT_PERCENTAGE / 100
        if self.order_type == OrderType.DELIVERY.name:
            self.delivery_charge = settings.DELIVERY_CHARGE
        self.grand_total = self.order_total + self.delivery_charge - self.order_discount
        self.save()

    def save(self, *args, **kwargs):
        '''
        Save order with unique order number using UUID
        '''
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order_number = models.ForeignKey(Order, null=False, blank=False,
                                     on_delete=models.CASCADE,
                                     related_name='lineitems')
    product_id = models.ForeignKey(Product, null=False, blank=False,
                                   on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    order_item_total = models.DecimalField(max_digits=6, decimal_places=2,
                                           null=False, blank=False,
                                           editable=False)

    def save(self, *args, **kwargs):
        '''
        Override the original save method to set the lineitem total
        and update the order total.
        '''
        self.order_item_total = self.product_id.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_id.name} from order {self.order_number.order_number}'
