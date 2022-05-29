import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from cart.contexts import cart_contents

from checkout.forms import OrderForm

# Create your views here.


def get_stripe_keys(request):
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
