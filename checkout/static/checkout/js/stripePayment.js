document.addEventListener('DOMContentLoaded', async () => {
    await mountStripeElement();
});

async function getStripeKeys() {
    const response = await fetch('/checkout/stripe/keys/');
    const keys = await response.json();
    return keys;
}

async function mountStripeElement() {
    const stripeKeys = await getStripeKeys();
    const stripe = Stripe(stripeKeys.publishable_key);
    const options = {
        appearance: {
            theme: 'flat',
            variables: {
                colorPrimary: 'var(--color-salmon)',
                colorBackground: '#ffffff',
                colorText: 'var(--color-salmon)',
                colorDanger: '#df1b41',
                fontFamily: 'PT Sans, sans-serif',
                spacingUnit: '2px',
                borderRadius: '4px',
            }
        },
    };

    const elements = stripe.elements(options);
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');

    return cardElement;
}