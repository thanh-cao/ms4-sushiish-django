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
            activateAddToCartButton(() => offCanvas.hide());
        });
    });

    document.getElementById('product-offcanvas').addEventListener('hidden.bs.offcanvas', () => {
        offCanvasBody.innerHTML = '';
    })
});

function activateAddToCartButton(callback) {
    document.querySelector('form.add-to-cart').addEventListener('submit', async (e) => {
        e.preventDefault();
        let form = e.target;
        let url = form.getAttribute('action');
        let method = form.getAttribute('method');
        let data = new FormData(form);
    
        await fetch(url, {
            method: method,
            body: data
        }).then(res => res.json());
        
        callback();
    });
}

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
