import json
import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render, reverse
from cart.contexts import cart_contents

from checkout.forms import OrderForm
from .models import Order, OrderLineItem, OrderType
from products.models import Product

# Create your views here.


def get_stripe_keys(request):
    '''
    This view returns stripe public and secret keys
    '''
    publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    current_cart = cart_contents(request)
    grand_total = current_cart['grand_total']
    stripe_total = round(grand_total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        automatic_payment_methods={
            'enabled': True,
        }
    )

    stripe_keys = {
        'publishable_key': publishable_key,
        'client_secret': intent.client_secret,
    }
    return JsonResponse(stripe_keys)


def update_order_type(request):
    '''
    This view updates the order type in the session and sends a json back
    to the client with order summary info in order to dynamically update
    the order charge upon changing the order type
    '''
    order_info = request.session.get('order_info', {})
    order_type = request.POST.get('order-type')
    order_info['order_type'] = order_type
    request.session['order_info'] = order_info

    order_summary = cart_contents(request)
    order_summary.pop('cart_items')
    return JsonResponse({'order_info': order_info,
                         'order_summary': order_summary})


def update_order_info(request):
    '''
    This view updates the order info in the session
    and sends a json back to the client
    '''
    order_info = request.session.get('order_info', {})
    order_type = request.POST.get('order-type')
    order_note = request.POST.get('order-note')
    expected_date = request.POST.get('expected-done-date')
    expected_time = request.POST.get('expected-done-time')

    if order_type is None or expected_date == '' or expected_time == '':
        error_message = JsonResponse(
            {'error': 'Please fill out all required fields'})
        return HttpResponse(status=400, content=error_message)

    order_info = {
        'order_type': order_type,
        'order_note': order_note,
        'expected_done_date': expected_date,
        'expected_done_time': expected_time,
    }
    request.session['order_info'] = order_info
    order_info = JsonResponse(order_info)
    return HttpResponse(status=200, content=order_info)


def checkout(request):
    '''
    This view renders the checkout page and handles order form submission
    after payment with Stripe is successful
    '''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        order_info = request.session.get('order_info')

        if form.is_valid():
            order = form.save(commit=False)
            if order_info['order_type'] == 'delivery':
                order.order_type = OrderType.DELIVERY.name
            else:
                order.order_type = OrderType.PICKUP.name
            # order.order_type = order_info['order_type']
            order.order_note = order_info['order_note']
            order.expected_done_date = order_info['expected_done_date']
            order.expected_done_time = order_info['expected_done_time']
            order.save()

            for item in cart_contents(request)['cart_items']:
                try:
                    order_line_item = OrderLineItem(
                        order_number=order,
                        product_id=item['product'],
                        quantity=item['quantity'],
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    order.delete()
                    return redirect(reverse('view_cart'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
    else:
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('products')

        order_form = OrderForm()
        context = {
            'order_form': order_form
        }
        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    '''
    This view renders the checkout success page
    '''
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if 'cart' in request.session:
        del request.session['cart']
    if 'order_info' in request.session:
        del request.session['order_info']

    context = {
        'order': order,
        'save_info': save_info,
    }
    return render(request, 'checkout/checkout-success.html', context)


@require_POST
def cache_checkout_data(request):
    '''
    This view caches the order info in the session
    '''
    try:
        stripe_pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(stripe_pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(content=e, status=400)
