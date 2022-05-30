from django.conf import settings
from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    '''
    This view renders shopping cart
    '''
    cart = request.session.get('cart', {})
    order_info = request.session.get('order_info')
    order_type = 'pickup'

    if order_info:
        order_type = order_info['order_type']

    cart_items = []
    order_total = 0
    product_count = 0
    order_discount = 0
    delivery_charge = Decimal(settings.DELIVERY_CHARGE) if (
        order_type == 'delivery') else 0
    grand_total = 0  # order_total + delivery_charge - order_discount

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

    if order_total >= settings.ORDER_DISCOUNT_THRESHOLD:
        order_discount = order_total * \
            Decimal(settings.ORDER_DISCOUNT_PERCENTAGE / 100)

    grand_total = order_total + delivery_charge - order_discount

    context = {
        'cart_items': cart_items,
        'order_total': order_total,
        'product_count': product_count,
        'delivery_charge': delivery_charge,
        'order_discount': order_discount,
        'discount_percentage': settings.ORDER_DISCOUNT_PERCENTAGE,
        'grand_total': grand_total,
    }
    return context
