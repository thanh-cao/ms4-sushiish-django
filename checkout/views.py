from django.shortcuts import redirect, render

from checkout.forms import OrderForm

# Create your views here.


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
