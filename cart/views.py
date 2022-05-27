from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from .contexts import cart_contents

# Create your views here.


def view_cart(request):
    '''
    This view renders shopping cart
    '''
    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    '''
    This view adds product to cart and saves it to session called cart
    and then send a json back to the client
    '''
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

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
