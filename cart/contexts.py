from django.conf import settings
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    '''
    This view renders shopping cart
    '''
    cart = request.session.get('cart', {})
    shipping_method = 'pickup'
    cart_items = []
    order_total = 0
    product_count = 0
    delivery_charge = settings.DELIVER_CHARGE if (
        shipping_method == 'delivery') else 0.00
    grand_total = 0  # delivery_charge + order total

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        order_item_total = quantity * product.price
        order_total += quantity * product.price
        product_count += quantity
        cart_items.append({
            'id': product_id,
            'quantity': quantity,
            'product': product,
            'order_item_total': order_item_total,
        })

    if order_total < settings.ORDER_DISCOUNT_THRESHOLD:
        if shipping_method == 'delivery':
            grand_total = order_total + settings.DELIVERY_CHARGE
        else:
            grand_total = order_total
    elif order_total >= settings.ORDER_DISCOUNT_THRESHOLD:
        if shipping_method == 'delivery':
            grand_total = order_total + settings.DELIVERY_CHARGE - \
                (order_total * Decimal(settings.ORDER_DISCOUNT_PERCENTAGE / 100))
        else:
            grand_total = order_total - \
                (order_total * Decimal(settings.ORDER_DISCOUNT_PERCENTAGE / 100))

    context = {
        'cart_items': cart_items,
        'order_total': order_total,
        'product_count': product_count,
        'delivery_charge': delivery_charge,
        'grand_total': grand_total,
    }
    return context
