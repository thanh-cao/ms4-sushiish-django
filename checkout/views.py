import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render

from checkout.forms import OrderForm

# Create your views here.


def get_stripe_keys(request):
    publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    secret_key = settings.STRIPE_SECRET_KEY
    stripe_keys = {
        'publishable_key': publishable_key,
        'secret_key': secret_key
    }
    return JsonResponse(stripe_keys)


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
