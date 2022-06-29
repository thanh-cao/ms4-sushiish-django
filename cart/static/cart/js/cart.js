document.addEventListener('DOMContentLoaded', async () => {
    activateQuantityChange();
    activateQuantityUpdate();
    activateRemoveFromCartButtons();

    if (document.querySelector('form#order-info-form')) {
        // handle selecting order type to be delivered or pickup
        document.querySelectorAll('input[name="order-type"]').forEach(input => {
            input.addEventListener('change', handleOrderTypeChange);
        });

        document.querySelector('input[type="time"]').addEventListener('change', handleTimeChange);

        // toggle add note field
        const orderNoteTextArea = document.querySelector('textarea[name="order-note"]');
        if (orderNoteTextArea.value.trim().length > 0) {
            orderNoteTextArea.parentElement.classList.remove('d-none');
        }
        document.querySelector('.add-note-btn').addEventListener('click', (e) => {
            e.preventDefault();
            orderNoteTextArea.parentElement.classList.toggle('d-none');
        });

        // handle processing order for checkout
        document.querySelector('#checkout-btn').addEventListener('click', handleProceedToCheckout);
    }
});

function activateQuantityChange() {
    document.querySelectorAll('.btn-quantity[data-type="minus"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            let target = btn.getAttribute('data-item_id');
            let closestInput = btn.closest('.input-group').querySelector(`input[data-item_id="${target}"]`);
            let currentValue = parseInt(closestInput.value);
            if (currentValue > 1) {
                closestInput.value = currentValue - 1;
            }
        });
    });

    document.querySelectorAll('.btn-quantity[data-type="plus"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            let target = btn.getAttribute('data-item_id');
            let closestInput = btn.closest('.input-group').querySelector(`input[data-item_id="${target}"]`);
            let currentValue = parseInt(closestInput.value);
            if (currentValue < closestInput.getAttribute('max')) {
                closestInput.value = currentValue + 1;
            }
        });
    });

    document.querySelectorAll('input.input-number').forEach(input => {
        input.addEventListener('change', (e) => {
            let input = document.querySelector('input.input-number');

            let value = parseInt(e.target.value);
            let max = e.target.getAttribute('max');
            let min = e.target.getAttribute('min');
            if (value > max) {
                input.value = max;
            } else if (value < min) {
                input.value = min;
            }
        });
    });
}

function activateRemoveFromCartButtons() {
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            let form = btn.parentElement;
            let url = form.getAttribute('action');
            let method = form.getAttribute('method');
            let csfrToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
            let data = new FormData();
            data.append('csrfmiddlewaretoken', csfrToken);
            let result = await fetch(url, {
                method: method,
                body: data
            });
            if (result.status === 200) {
                location.reload();
            }
        });
    });
}

function activateQuantityUpdate() {
    document.querySelectorAll('.update-quantity-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            let target = btn.getAttribute('data-form_id');
            let quantityForm = document.querySelector(`form#${target}`);
            quantityForm.submit();
        });
    });
}

async function handleOrderTypeChange(event) {
    event.preventDefault();
    const value = event.target.value;
    const data = new FormData();
    const csfrToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    data.append('order-type', value);
    data.append('csrfmiddlewaretoken', csfrToken);
    const url = '/checkout/update_order_type/';

    const result = await fetch(url, {
        method: 'POST',
        body: data,
    }).then(response => response.json());
    const orderSummary = result.order_summary;

    document.querySelector('#order-total-cart').innerHTML = `$${parseFloat(orderSummary.order_total).toFixed(2)}`;
    document.querySelector('#delivery-charge').innerHTML = `$${parseFloat(orderSummary.delivery_charge).toFixed(2)}`;
    document.querySelector('#grand-total').innerHTML = `$${parseFloat(orderSummary.grand_total).toFixed(2)}`;
}

function handleTimeChange(e) {
    const chosenTime = e.target.value;
    const minTime = e.target.getAttribute('min');
    const maxTime = e.target.getAttribute('max');
    const errorDiv = e.target.parentElement.parentElement.previousElementSibling.previousElementSibling.previousElementSibling;

    if (chosenTime < minTime || chosenTime > maxTime) {
        errorDiv.innerText = `Time must be between ${minTime} and ${maxTime}`;
        e.target.value = chosenTime < minTime ? minTime : maxTime;
    } else {
        errorDiv.innerText = '';
    }
}

async function handleProceedToCheckout(event) {
    event.preventDefault();
    const form = document.querySelector('#order-info-form');
    const url = form.getAttribute('action');
    const method = form.getAttribute('method');
    const data = new FormData(form);

    const response = await fetch(url, {
        method: method,
        body: data
    });
    const result = await response.json();
    if (response.status === 200) {
        location.href = '/checkout/';
    } else if (response.status === 400) {
        document.querySelectorAll('#order-info-form .error-message').forEach(div => {
            div.innerText = result.error;
        });
    }
}