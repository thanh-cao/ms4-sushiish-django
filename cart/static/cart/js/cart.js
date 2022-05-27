document.addEventListener('DOMContentLoaded', async () => {
    activateQuantityChange();
    activateQuantityUpdate();
    activateRemoveFromCartButtons();
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

