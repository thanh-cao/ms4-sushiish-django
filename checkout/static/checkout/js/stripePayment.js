let stripe;
let elements;

document.addEventListener('DOMContentLoaded', async () => {
    const stripeKeys = await getStripeKeys();
    if (stripeKeys.publishable_key) {
        stripe = Stripe(stripeKeys.publishable_key);
        await mountStripeElement(stripeKeys);
        document.querySelector('button[type="submit"]').addEventListener('click', (event) => handlePaymentFormSubmit(event, stripeKeys));
    } else {
        document.querySelector('button[type="submit"]').disabled = true;
    }
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

function displayLoadingOverlay(value) {
    const loadingOverlay = document.querySelector('#loading-overlay');

    if (value) {
        loadingOverlay.style.visibility = 'visible';
        loadingOverlay.style.opacity = '0.7';
    } else {
        loadingOverlay.style.visibility = 'hidden';
        loadingOverlay.style.opacity = '0';
    }
}

// validateField() and validateCheckoutForm() are used display custom error messages
// for the fields in the payment form since the default validation messages by browser
// are disabled by stripe element.
function validateField(field, validation, message) {
    const feedbackDiv = field.parentElement.querySelector('.invalid-feedback');
    if (!validation) {
        console.log('validation failed');
        feedbackDiv.textContent = message;
        feedbackDiv.style.display = 'block';
        document.querySelector('#card-errors').innerHTML = 'Please check the all the fields and try again.';
        return false;
    } else {
        feedbackDiv.textContent = '';
        feedbackDiv.style.display = 'none';
        return true;
    }
}

function validateCheckoutForm() {
    const form = document.querySelector('#payment-form');
    if (form.checkValidity()) {
        return true;
    }
    const requiredFields = form.querySelectorAll('input[required]');
    let valid = true;

    requiredFields.forEach(field => {
        const validation = field.value !== '';
        valid = validateField(field, validation, 'This field is required.');
    });

    const emailField = form.querySelector('input[name="email"]');
    const emailValidation = emailField.value !== '' && emailField.checkValidity();
    valid = validateField(emailField, emailValidation, 'Please enter a valid email address.');

    const phoneField = form.querySelector('input[name="phone_number"]');
    const phoneValidation = phoneField.value !== '' && phoneField.checkValidity();
    valid = validateField(phoneField, phoneValidation, 'Please enter a valid phone number.');

    return valid;
}

async function handlePaymentFormSubmit(event, stripeKeys) {
    event.preventDefault();
    displayLoadingOverlay(true);
    const validated = validateCheckoutForm();

    if (validated) {
        const paymentForm = document.querySelector('#payment-form');
        const errorDiv = document.getElementById('card-errors');
        let stripeConfirmPaymentResult;
        cacheDataUrl = '/checkout/cache_checkout_data/';

        const csfrToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const saveInfo = document.querySelector('input[name="save-info"]') ? Boolean(document.querySelector('input[name="save-info"]').checked) : false;
        const cacheData = new FormData();
        cacheData.append('csrfmiddlewaretoken', csfrToken);
        cacheData.append('save_info', saveInfo);
        cacheData.append('client_secret', stripeKeys.client_secret);

        const formData = new FormData(paymentForm);

        try {
            const responseFromCache = await fetch(cacheDataUrl, {
                method: 'POST',
                body: cacheData,
            });

            if (responseFromCache.status === 200) {
                stripeConfirmPaymentResult = await stripe.confirmPayment({
                    elements,
                    redirect: 'if_required',
                    confirmParams: {
                        shipping: {
                            name: formData.get('full_name').trim(),
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
            }

            if (stripeConfirmPaymentResult.error) {
                displayLoadingOverlay(false);

                const errorHtml = `
            <span class="icon" role="alert">
            <i class="fas fa-times"></i>
            </span>
            <span>${stripeConfirmPaymentResult.error.message}</span>`;

                errorDiv.innerHTML = errorHtml;
            } else {
                if (stripeConfirmPaymentResult.paymentIntent.status === 'succeeded') {
                    const checkoutUrl = paymentForm.getAttribute('action');
                    formData.append('client_secret', stripeKeys.client_secret);

                    const response = await fetch(checkoutUrl, {
                        method: 'POST',
                        body: formData,
                    });
                    if (response.status === 200) {
                        displayLoadingOverlay(false);
                        const result = await response.json();
                        location.replace(`/checkout/success/${result.order_number}`);
                    } else {
                        displayLoadingOverlay(false);

                        errorDiv.innerHTML = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>Something went wrong. Please try again.</span>`;
                    }
                }
            }
        } catch (error) {
            displayLoadingOverlay(false);
            const errorHtml = `
            <span class="icon" role="alert">
            <i class="fas fa-times"></i>
            </span>
            <span>${error}</span>`;

            errorDiv.innerHTML = errorHtml;
        }
    } else {
        displayLoadingOverlay(false);
    }
}
