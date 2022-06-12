const activateQuantityChange = () => {
    document.querySelectorAll('.btn-quantity').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            let type = btn.getAttribute('data-type');
            changeQtyAddToCart(type);
        });
    });
    document.querySelector('input.input-number').addEventListener('change', (e) => {
        let input = document.querySelector('input.input-number');

        let value = parseInt(e.target.value);
        let max = e.target.getAttribute('max');
        let min = e.target.getAttribute('min');
        if (value > max) {
            input.value = max;
        } else if (value < min) {
            input.value = min;
        }
        changeQtyAddToCart('custom');
    });
};

const changeQtyAddToCart = (type) => {
    let input = document.querySelector('input.input-number');
    let quantity = parseInt(input.value);
    
    if (type === 'plus') {
        if (quantity < parseInt(input.getAttribute('max'))) {
            input.value = quantity + 1;
        }
        checkToDisableButton(parseInt(input.value), parseInt(input.getAttribute('max')), parseInt(input.getAttribute('min')));
    } else if (type === 'minus') {
        if (quantity > 1) {
            input.value = quantity - 1;
        }
        checkToDisableButton(parseInt(input.value), parseInt(input.getAttribute('max')), parseInt(input.getAttribute('min')));
    }

    calculateTotal(parseFloat(input.value));
};

const calculateTotal = (quantity) => {
    let total = document.querySelector('.add-total');
    let price = parseFloat(document.querySelector('.offcanvas-body .price').innerText.split('$')[1]);
    total.innerText = (price * quantity).toFixed(2);
};

const checkToDisableButton = (quantity, max, min) => {
    if (quantity === max) {
        document.querySelector('.btn-quantity[data-type="plus"]').setAttribute('disabled', 'true');
    } else {
        document.querySelector('.btn-quantity[data-type="plus"]').removeAttribute('disabled');
    }

    if (quantity === min) {
        document.querySelector('.btn-quantity[data-type="minus"]').setAttribute('disabled', 'true');
    } else {
        document.querySelector('.btn-quantity[data-type="minus"]').removeAttribute('disabled');
    }
};