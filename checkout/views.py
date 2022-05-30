import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from cart.contexts import cart_contents

from checkout.forms import OrderForm

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
    expected_date = request.POST.get('expected-date')
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
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('products')
    else:
        order_form = OrderForm()

        context = {
            'cart': cart,
            'order_form': order_form
        }
        return render(request, 'checkout/checkout.html', context)
