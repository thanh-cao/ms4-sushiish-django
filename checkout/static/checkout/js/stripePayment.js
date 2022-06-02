let stripe;
let elements;

document.addEventListener('DOMContentLoaded', async () => {
    const stripeKeys = await getStripeKeys();
    stripe = Stripe(stripeKeys.publishable_key);
    await mountStripeElement(stripeKeys);
    document.querySelector('#payment-form').addEventListener('submit', (event) => handlePaymentFormSubmit(event, stripeKeys));
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

async function handlePaymentFormSubmit(event, stripeKeys) {
    event.preventDefault();
    const errorDiv = document.getElementById('card-errors');

    cacheDataUrl = '/checkout/cache_checkout_data/';
    const csfrToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const saveInfo = Boolean(document.querySelector('input[name="save-info"]').checked);
    const cacheData = new FormData();
    cacheData.append('csrfmiddlewaretoken', csfrToken);
    cacheData.append('save-info', saveInfo);
    cacheData.append('client_secret', stripeKeys.client_secret);

    const formData = new FormData(event.target);

    try {

        const responseFromCache = await fetch(cacheDataUrl, {
            method: 'POST',
            body: cacheData,
        });

        const result = await stripe.confirmPayment({
            elements,
            redirect: 'if_required',
            confirmParams: {
                shipping: {
                    name: formData.get('full_name').trim(), // remove white space
                    phone: formData.get('phone_number').trim(),
                    address: {
                        line1: formData.get('street_address1').trim(),
                        line2: formData.get('street_address2').trim(),
                        city: formData.get('town_or_city').trim(),
                        postal_code: formData.get('postcode').trim(),
                        country: formData.get('country').trim(),
                    }
                },
                payment_method_data: {
                    billing_details: {
                        name: formData.get('full_name').trim(),
                        phone: formData.get('phone_number').trim(),
                        email: formData.get('email').trim(),
                        address: {
                            line1: formData.get('street_address1').trim(),
                            line2: formData.get('street_address2').trim(),
                            city: formData.get('town_or_city').trim(),
                            postal_code: formData.get('postcode').trim(),
                            country: formData.get('country').trim(),
                        }
                    }
                }
            },
        });
        if (result.error) {
            const errorHtml = `
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
    } catch (error) {
        const errorHtml = `
            <span class="icon" role="alert">
            <i class="fas fa-times"></i>
            </span>
            <span>${result.error.message}</span>`;

        errorDiv.innerHTML = errorHtml;
    }
}