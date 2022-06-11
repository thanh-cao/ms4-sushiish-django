import datetime
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse

from products.models import Product
from .contexts import cart_contents

# Create your views here.


def view_cart(request):
    '''
    This view renders shopping cart and datetime values
    for the input fields
    '''
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    max_date = today + datetime.timedelta(days=30)
    now = datetime.datetime.now().time()
    min_time = datetime.time(hour=13, minute=15)
    max_time = datetime.time(hour=21, minute=00)

    set_now_time = now
    if now < min_time or now > max_time:
        set_now_time = min_time

    context = {
        'today': today.strftime(
            '%Y-%m-%d') if now < max_time else tomorrow.strftime('%Y-%m-%d'),
        'max_date': max_date.strftime('%Y-%m-%d'),
        'now': set_now_time.strftime('%H:%M'),
        'min_time': min_time.strftime('%H:%M'),
        'max_time': max_time.strftime('%H:%M'),
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
    print('adjust_cart')
    quantity = int(request.POST.get('quantity'))
    print(quantity)
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, product_id):
    '''
    This view removes a product from the cart
    '''
    try:
        cart = request.session.get('cart', {})
        cart.pop(product_id)
        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
