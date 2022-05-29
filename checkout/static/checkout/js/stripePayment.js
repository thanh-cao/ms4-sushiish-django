let stripe;
let elements;

document.addEventListener('DOMContentLoaded', async () => {
    const stripeKeys = await getStripeKeys();
    stripe = Stripe(stripeKeys.publishable_key);
    await mountStripeElement(stripeKeys);
    document.querySelector('#payment-form').addEventListener('submit', handlePaymentFormSubmit);
});

async function getStripeKeys() {
    const response = await fetch('/checkout/stripe/keys/');
    const keys = await response.json();
    return keys;
}

async function mountStripeElement(stripeKeys) {
    const options = {
        clientSecret: stripeKeys.client_secret,
        appearance: {
            theme: 'stripe',
            labels: 'floating',
            variables: {
                colorPrimary: '#44b5aa',
                colorBackground: '#ffffff',
                colorText: '#000',
                colorDanger: '#ff7e6b',
                colorSuccess: '#44b5aa',
                fontFamily: 'PT Sans, sans-serif',
                spacingUnit: '2px',
                borderRadius: '4px',
            }
        },
    };

    elements = stripe.elements(options);
    const cardElement = elements.create('payment');
    cardElement.mount('#card-element');
}

async function handlePaymentFormSubmit(event) {
    event.preventDefault();

    const result = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: "checkout/success/",
        },
    });
    if (result.error) {
        var errorDiv = document.getElementById('card-errors');
        var errorHtml = `
            <span class="icon" role="alert">
            <i class="fas fa-times"></i>
            </span>
            <span>${result.error.message}</span>`;

        errorDiv.innerHTML = errorHtml;
    } else {
        if (result.paymentIntent.status === 'succeeded') {
            document.querySelector('#payment-form').submit();
        }
    }
}
