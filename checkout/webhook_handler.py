import json
import time
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from checkout.models import Order, OrderLineItem
from products.models import Product
from profiles.forms import AddressForm
from profiles.models import UserProfile
from profiles.views import resetting_default_address


class StripeWebhook_Handler:
    '''
    Stripe webhook handler
    '''

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        '''
        Send the order confirmation email
        '''
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order,
             'sushiish_contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        '''
        Handle a generic/unknown/unexpected webhook event
        '''
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_success(self, event):
        '''
        Handle the payment_intent.succeeded webhook from Stripe
        '''
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                address_data = {
                    'phone_number': shipping_details.phone,
                    'street_address1': shipping_details.address.line1,
                    'street_address2': shipping_details.address.line2,
                    'town_or_city': shipping_details.address.city,
                    'postcode': shipping_details.address.postal_code,
                    'country': shipping_details.address.country,
                    'country_area': shipping_details.address.country_area,
                    'isDefault': True,
                }

                address_form = AddressForm(address_data)
                if address_form.is_valid():
                    address = address_form.save(commit=False)
                    address.profile_id = profile
                    address.save()
                    resetting_default_address(address, profile)

        # Create the order and attempts 5 times
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    grand_total=grand_total,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    stripe_pid=pid,
                )
                for item_id, quantity in json.loads(cart).items():
                    print(item_id, quantity)
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order_number=order,
                        product_id=product,
                        quantity=quantity,
                    )
                    order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_failure(self, event):
        '''
        Handle the payment_intent.payment_failed webhook from Stripe
        '''
        return HttpResponse(
            content=f'Payment failed: {event["type"]}',
            status=200)
