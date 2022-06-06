from django.contrib import admin
from .models import Order, OrderLineItem
# Register your models here.


class OrderLineAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('order_item_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline,)
    readonly_fields = ('order_number', 'create_date', 'delivery_charge',
                       'order_total', 'order_discount', 'grand_total',
                       'stripe_pid',)
    fields = ('order_number', 'user_profile', 'full_name', 'email',
              'phone_number', 'street_address1', 'street_address2',
              'town_or_city', 'postcode', 'country', 'order_type',
              'delivery_charge', 'order_total', 'order_discount',
              'grand_total', 'create_date', 'expected_done_date',
              'expected_done_time', 'order_note', 'stripe_pid',)
    list_display = ('order_number', 'full_name', 'email', 'phone_number',
                    'order_total', 'order_discount', 'grand_total',
                    'order_type', 'delivery_charge', 'create_date')
    ordering = ('-create_date', 'order_type',)
    search_fields = ('order_number', 'full_name', 'email', 'phone_number',
                     'street_address1', 'street_address2', 'town_or_city',
                     'postcode', 'country', 'order_type', 'delivery_charge',
                     'order_total', 'order_discount', 'grand_total',
                     'create_date', 'expected_done_date', 'expected_done_time')


admin.site.register(Order, OrderAdmin)
