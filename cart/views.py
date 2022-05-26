from django.http import JsonResponse
from django.shortcuts import render

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

    request.session['cart'] = cart
    return JsonResponse({'cart': request.session['cart']})
