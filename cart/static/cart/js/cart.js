document.addEventListener('DOMContentLoaded', async () => {
    activateQuantityChange();
    activateQuantityUpdate();
    activateRemoveFromCartButtons();
    document.querySelectorAll('input[name="order-type"]').forEach(input => {
        input.addEventListener('change', handleOrderTypeChange);
    });
    document.querySelector('#checkout-btn').addEventListener('click', handleProceesToCheckout);
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
};

function activateRemoveFromCartButtons() {
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            console.log('remove from cart');
            e.preventDefault();
            let form = btn.parentElement;
            console.log(form);
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
            console.log(quantityForm);
            quantityForm.submit();
        });
    });
};

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
    
    document.querySelector('#order-total').innerHTML = `$${parseFloat(orderSummary.order_total).toFixed(2)}`;
    document.querySelector('#delivery-charge').innerHTML = `$${parseFloat(orderSummary.delivery_charge).toFixed(2)}`;
    document.querySelector('#grand-total').innerHTML = `$${parseFloat(orderSummary.grand_total).toFixed(2)}`;
    orderSummary.order_discount > 0 ? document.querySelector('#order-discount').innerHTML = `- $${parseFloat(orderSummary.order_discount).toFixed(2)}` : null;
}

async function handleProceesToCheckout(event) {
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
        document.querySelector('#order-info-form .error-message').innerHTML = result.error;
    }
}