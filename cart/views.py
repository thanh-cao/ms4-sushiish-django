import datetime
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse

from products.models import Product
from .contexts import cart_contents

# Create your views here.


def get_earliest_possible_done_by():
    '''
    This function returns the earliest possible time for the order to be done.
    Earliest possible time is calculated by now time plus 30mins so that
    kitchen has enough time to prepare the order. If earliest possible
    time is after closing time, then earliest possible time is set to
    opening time tomorrow. If earliest possible time is before opening
    time, then earliest possible time is set to opening time today.

    Possible pickup/delivery times are between 13:15 and 21:00, which is
    15 mins after opening time to give enough time for kitchen to prepare
    the order in the opening hours.
    '''
    earliest_possible = datetime.datetime.now() \
        + datetime.timedelta(minutes=30)
    opening_time = datetime.time(hour=13, minute=15)
    closing_time = datetime.time(hour=21, minute=00)
    today = datetime.date.today()
    opening_time_datetime = datetime.datetime.combine(today, opening_time)
    closing_time_datetime = datetime.datetime.combine(today, closing_time)

    if earliest_possible < opening_time_datetime:
        earliest_possible = opening_time_datetime
    elif earliest_possible > closing_time_datetime:
        earliest_possible = opening_time_datetime + datetime.timedelta(days=1)

    return earliest_possible


def get_prefilled_datetime_input(request):
    '''
    This function returns datetime values to be prefilled in the input fields.
    The value returned is the earliest possible time for the order to be done
    or the time stored in session, previously set by the user if it is after
    the earliest possible time.
    '''
    earliest_possible = get_earliest_possible_done_by()
    prefilled_datetime_input = earliest_possible

    order_info = request.session.get('order_info', {})

    if order_info:
        saved_in_session_done_time = order_info['expected_done_time'] if \
            order_info['expected_done_time'] else None
        saved_in_session_done_date = order_info['expected_done_date'] if \
            order_info['expected_done_date'] else None

        if saved_in_session_done_time and saved_in_session_done_date:
            time = datetime.datetime.strptime(
                saved_in_session_done_time, '%H:%M').time()
            date = datetime.datetime.strptime(
                saved_in_session_done_date, '%Y-%m-%d')
            saved_expected_done_by = datetime.datetime.combine(date, time)

            if saved_expected_done_by > earliest_possible:
                prefilled_datetime_input = saved_expected_done_by
    return prefilled_datetime_input


def view_cart(request):
    '''
    This view renders shopping cart and datetime values
    for the input fields
    '''
    today = datetime.date.today()
    max_date = today + datetime.timedelta(days=30)

    opening_time = datetime.time(hour=13, minute=15)
    closing_time = datetime.time(hour=21, minute=00)

    prefilled_datetime_input = get_prefilled_datetime_input(request)
    print(prefilled_datetime_input)

    context = {
        'today': today.strftime('%Y-%m-%d'),
        'set_date_input': prefilled_datetime_input.strftime('%Y-%m-%d'),
        'max_date': max_date.strftime('%Y-%m-%d'),
        'set_time_input': prefilled_datetime_input.strftime('%H:%M'),
        'opening_time': opening_time.strftime('%H:%M'),
        'closing_time': closing_time.strftime('%H:%M'),
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    '''
    This view adds product to cart and saves it to session called cart
    and then send a json back to the client
    '''
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, pk=product_id)

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
        messages.success(
            request, f'{product.name} quantity updated to {cart[product_id]}')
    else:
        cart[product_id] = quantity
        messages.success(request, f'{product.name} added to cart')

    order_total = cart_contents(request)['order_total']
    request.session['cart'] = cart
    return JsonResponse({'cart': request.session['cart'],
                         'order_total': order_total})


def adjust_cart(request, product_id):
    '''
    This view adjusts the quantity of a product in the cart
    '''
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, pk=product_id)

    if quantity > 0:
        cart[product_id] = quantity
        messages.success(
            request, f'{product.name} quantity updated to {quantity}')
    else:
        cart.pop(product_id)
        messages.success(request, f'{product.name} removed from cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, product_id):
    '''
    This view removes a product from the cart
    '''
    try:
        if product_id == '0':
            request.session['cart'] = {}
            messages.success(request, 'Your cart is now empty')
            return redirect(reverse('view_cart'))
        else:
            product = get_object_or_404(Product, pk=product_id)
            cart = request.session.get('cart', {})
            cart.pop(product_id)
            request.session['cart'] = cart
            messages.success(request, f'{product.name} removed from cart')
            return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing {product.name} from cart')
        return HttpResponse(status=500)
