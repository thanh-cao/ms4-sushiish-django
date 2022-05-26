from django.conf import settings
from decimal import Decimal


def cart_contents(request):
    '''
    This view renders shopping cart
    '''
    shipping_method = 'pickup'
    cart_items = []
    total = 0
    product_count = 0
    grand_total = 0

    if total < settings.ORDER_DISCOUNT_THRESHOLD:
        if shipping_method == 'delivery':
            grand_total = total + settings.DELIVERY_CHARGE
        else:
            grand_total = total
    elif total >= settings.ORDER_DISCOUNT_THRESHOLD:
        if shipping_method == 'delivery':
            grand_total = total + settings.DELIVERY_CHARGE - \
                (total * Decimal(settings.ORDER_DISCOUNT_PERCENTAGE / 100))
        else:
            grand_total = total - \
                (total * Decimal(settings.ORDER_DISCOUNT_PERCENTAGE / 100))

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }
    return context
