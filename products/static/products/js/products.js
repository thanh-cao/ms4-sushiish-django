// calculate price per total order item 
document.addEventListener('DOMContentLoaded', async (e) => {
    let offCanvas = new bootstrap.Offcanvas(document.getElementById('product-offcanvas'));
    let offCanvasBody = document.querySelector('.offcanvas-body');

    document.querySelectorAll('[data-bs-toggle="offcanvas"]').forEach(card => {
        card.addEventListener('click', async (e) => {
            e.preventDefault();
            let url = card.getAttribute('data-product-url');
            const productDetailHtml = await fetch(url).then(res => res.text());
            offCanvasBody.innerHTML = productDetailHtml;
            offCanvas.show();

            activateQuantityChange();
        });
    });

    document.getElementById('product-offcanvas').addEventListener('hidden.bs.offcanvas', () => {
        offCanvasBody.innerHTML = '';
    })
});

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
        if (quantity < input.getAttribute('max')) {
            input.value = quantity + 1;
        }
    } else if (type === 'minus') {
        if (quantity > 1) {
            input.value = quantity - 1;
        }
    }
    calculateTotal(parseFloat(input.value));
};

const calculateTotal = (quantity) => {
    let total = document.querySelector('.add-total');
    let price = parseFloat(document.querySelector('.offcanvas-body .price').innerText.split('$')[1]);
    total.innerText = (price * quantity).toFixed(2);
};

// Filter by allergy
function filterProducts(productList, allergy) {
    let filteredProducts = productList.filter(product => {
        let productAllergies = product.fields.allergies;
        return !productAllergies.includes(allergy);
    });
    return filteredProducts;
}
document.querySelectorAll('.allergy-checkbox').forEach(async checkbox => {
    const productList = await fetch('/products/json/').then(res => res.json());
    checkbox.addEventListener('change', async () => {
        let filteredProducts;
        if (checkbox.checked) {
            filteredProducts = filterProducts(productList, checkbox.value);
        } else {
            filteredProducts = productList;
        }
        const productListingContainer = document.querySelector('.product-listing-container');
        productListingContainer.innerHTML = '';
        
        filteredProducts.forEach(product => {
            const productId = product.pk;
            product = product.fields;
            let productCard = document.createElement('div');
            productCard.classList.add('col-12', 'col-md-6');

            const productAllergiesHtml = product.allergies.length > 0 ? product.allergies.map(allergy => {
                return `<span class="allergy-tag">${allergy}</span>`;
            }).join('') : null;

            productCard.innerHTML = `              
                    <a href="/products/${productId}" class="text-decoration-none text-black"
                        data-bs-toggle="offcanvas" data-product-url="/products/${productId}">
                        <div class="card product-card">
                            <div class="card-body">
                                <div class="product-title fs-5 text-salmon fw-bold">${product.name}</div>                            
                                <div class="product-allergies my-2">
                                    ${productAllergiesHtml ? productAllergiesHtml : ''}
                                </div>                               
                                <div class="product-text">${product.description}</div>
                                <div class="price fw-bold">
                                    $${parseFloat(product.price).toFixed(2)}
                                </div>
                            </div>
                            <div class="product-img-container">
                                <div class="product-img" style="background-image: url('/media/${product.image}')">
                                </div>
                            </div>
                        </div>
                    </a>         
                `;
            productListingContainer.appendChild(productCard);
        });
    });
});
