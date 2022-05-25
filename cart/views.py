from django.shortcuts import render

# Create your views here.


def view_cart(request):
    '''
    This view renders shopping cart
    '''
    return render(request, 'cart/cart.html')
