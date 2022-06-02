import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWebhook_Handler


@require_POST
@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhooks for the checkout app.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=400, content=e)

    # Set up a webhook handler
    wb_handler = StripeWebhook_Handler(request)

    # Map webhook events to relevant handler functions
    event_handler_map = {
        'payment_intent.succeeded': wb_handler.handle_payment_success,
        'payment_intent.payment_failed': wb_handler.handle_payment_failure,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_handler_map.get(event_type, wb_handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
