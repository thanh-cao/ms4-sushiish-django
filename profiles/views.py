from django.shortcuts import get_object_or_404, render
from checkout.models import Order
from profiles.forms import AddressForm, UserDetailsForm

from profiles.models import UserProfile

# Create your views here.


def profile(request):
    '''
    View to render user's profile page with all their info
    and order history
    '''
    profile = get_object_or_404(UserProfile, user=request.user)
    addresses = profile.address_set.all()
    orders = profile.orders.all()
    user_form = UserDetailsForm(instance=request.user)
    address_form = AddressForm()
    context = {
        'profile': profile,
        'orders': orders,
        'addresses': addresses,
        'user_detail_form': user_form,
        'address_form': address_form,
    }
    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    '''
    Render user's past order details
    '''
    order = get_object_or_404(Order, order_number=order_number)

    context = {
        'page_type': 'history',
        'order': order,
    }

    return render(request, 'checkout/checkout-success.html', context)
