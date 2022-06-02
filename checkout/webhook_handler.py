from django.http import HttpResponse


class StripeWebhook_Handler:
    '''
    Stripe webhook handler
    '''

    def __init__(self, request):
        self.request = request

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
        print(intent)
        print('Payment succeeded!')
        return HttpResponse(
            content=f'Payment succeeded',
            status=200)

    def handle_payment_failure(self, event):
        '''
        Handle the payment_intent.payment_failed webhook from Stripe
        '''
        print('Payment failed.')
        return HttpResponse(
            content=f'Payment failed',
            status=200)
