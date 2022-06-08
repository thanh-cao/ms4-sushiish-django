from django.shortcuts import get_object_or_404, redirect, render
from checkout.models import Order
from profiles.forms import AddressForm, UserDetailsForm

from profiles.models import Address, UserProfile

# Create your views here.


def profile(request):
    '''
    View to render user's profile page with all their info
    and order history
    '''
    profile = get_object_or_404(UserProfile, user=request.user)
    addresses = profile.address_set.all()
    orders = profile.orders.all()
    context = {
        'profile': profile,
        'orders': orders,
        'addresses': addresses,
    }
    return render(request, 'profiles/profile.html', context)


def update_user_details(request):
    '''
    Update user details
    '''
    if request.method == 'POST':
        try:
            user_form = UserDetailsForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('profile')
        except ValueError:
            pass
        except Exception as e:
            print(e)  # TODO: message toast error
    else:
        user_form = UserDetailsForm(instance=request.user)

    context = {
        'user_detail_form': user_form,
    }

    return render(request, 'profiles/includes/update-info-form.html', context)


def create_address(request):
    '''
    Create a new address for the user
    '''
    if request.method == 'POST':
        try:
            profile = get_object_or_404(UserProfile, user=request.user)
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.profile_id = profile
                address.save()
                if address.isDefault is True:
                    # if newly added address is set as default,
                    # set all other addresses to not default
                    addresses = profile.address_set.all().exclude(id=address.id)
                    for addr in addresses:
                        addr.isDefault = False
                        addr.save()
                return redirect('profile')
        except ValueError:
            pass
        except Exception as e:
            print(e)  # TODO: message toast error
    else:
        form = AddressForm()

    context = {
        'address_form': form,
    }

    return render(request, 'profiles/includes/address-form.html', context)


def update_address(request, address_id):
    '''
    Update user's address
    '''
    profile = get_object_or_404(UserProfile, user=request.user)
    address = get_object_or_404(Address, id=address_id)

    if request.method == 'POST':
        try:
            form = AddressForm(request.POST, instance=address)
            if form.is_valid():
                address = form.save()
                if address.isDefault is True:
                    # if currently editted address is set as default,
                    # set all other addresses to not default
                    addresses = profile.address_set.all().exclude(id=address.id)
                    for addr in addresses:
                        addr.isDefault = False
                        addr.save()
                return redirect('profile')
        except ValueError:
            pass
        except Exception as e:
            print(e)  # TODO: message toast error
    else:
        form = AddressForm(instance=address)

    context = {
        'address': address,
        'address_form': form,
    }

    return render(request, 'profiles/includes/address-form.html', context)


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
