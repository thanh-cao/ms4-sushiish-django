from django.contrib import messages
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
            messages.error(request, 'Error updating user details')
            pass
        except Exception as e:
            messages.error(request, e)
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
                    # if this address is set as default,
                    # set all other addresses to not default
                    resetting_default_address(address, profile)
                messages.success(request, 'Address created successfully')
                return redirect('profile')
        except ValueError:
            messages.error(request, 'Error creating address')
            pass
        except Exception as e:
            messages.error(request, e)
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
                    resetting_default_address(address, profile)
                messages.success(request, 'Address updated successfully')
                return redirect('profile')
        except ValueError:
            messages.error(request, 'Error updating address')
            pass
        except Exception as e:
            messages.error(request, e)
    else:
        form = AddressForm(instance=address)

    context = {
        'address': address,
        'address_form': form,
    }

    return render(request, 'profiles/includes/address-form.html', context)


def delete_address(request, address_id):
    '''
    Delete user's address
    '''
    address = get_object_or_404(Address, id=address_id)
    profile = get_object_or_404(UserProfile, user=request.user)
    if address.profile_id == profile:
        address.delete()
        messages.success(request, 'Address deleted successfully')
        return redirect('profile')
    else:
        messages.error(request, 'Error deleting address')
        return redirect('profile')


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


def resetting_default_address(default_address, profile):
    '''
    This view resets the default address of the user
    '''
    addresses = profile.address_set.all().exclude(id=default_address.id)
    if addresses.count() > 0:
        for addr in addresses:
            addr.isDefault = False
            addr.save()
