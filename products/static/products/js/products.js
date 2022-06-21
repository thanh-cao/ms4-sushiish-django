const productCardList = document.querySelectorAll('.col-12.col-md-6.product');

document.addEventListener('DOMContentLoaded', async (e) => {
    // initialize Bootstrap's offcanvas section
    let offCanvas = new bootstrap.Offcanvas(document.getElementById('product-offcanvas'));
    let offCanvasBody = document.querySelector('.offcanvas-body');

    // Add event listener to each product card to load product details to offcanvas 
    // upon click and display the details. Activate listeners for quantity change buttons
    // and add to cart button.
    document.querySelectorAll('[data-bs-toggle="offcanvas"]').forEach(card => {
        card.addEventListener('click', async (e) => {
            e.preventDefault();
            let url = card.getAttribute('data-product-url');
            const productDetailHtml = await fetch(url).then(res => res.text());
            offCanvasBody.innerHTML = productDetailHtml;
            offCanvas.show();

            activateQuantityChange(); // from quantityInput.js file
            activateAddToCartButton(() => { 
                offCanvas.hide();
                location.reload();
            });
        });
    });

    // Event listener when Bootstrap's offcanvas is closed, to clear the offcanvas body content
    document.getElementById('product-offcanvas').addEventListener('hidden.bs.offcanvas', () => {
        offCanvasBody.innerHTML = '';
    });

    // Event lister for filtering product list by allergies
    document.querySelectorAll('.allergy-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handleAllergySelect);
    });
});

function activateAddToCartButton(callback) {
    document.querySelector('form.add-to-cart').addEventListener('submit', async (e) => {
        e.preventDefault();
        let form = e.target;
        let url = form.getAttribute('action');
        let method = form.getAttribute('method');
        let data = new FormData(form);

        let result = await fetch(url, {
            method: method,
            body: data
        }).then(res => res.json());

        document.querySelector('#order-total').innerHTML = result.order_total;
        callback();
    });
}

// functions below are used to filter product list by multiple allergies
function generateSelectedAllergyFilterList() {
    const selectedAllergies = document.querySelectorAll('input.allergy-checkbox:checked');
    let allergies = [];
    selectedAllergies.forEach(allergy => {
        allergies.push(allergy.value);
    });
    return allergies;
}

function extractAllergiesFromProductCard(productCard) {
    let allergies = [];
    productCard.querySelectorAll('.allergy-tag').forEach(allergyTag => {
        allergies.push(allergyTag.textContent);
    });
    return allergies;
}

function filterProductsByAllergies(productCardList, allergies) {
    let filteredProducts = [];
    let allergiesSet = new Set(allergies);
    productCardList.forEach(productCard => {
        let productAllergies = extractAllergiesFromProductCard(productCard);
        let productAllergiesSet = new Set(productAllergies);
        let intersection = new Set([...productAllergiesSet].filter(allergy => allergiesSet.has(allergy)));
        if (intersection.size === 0) {
            filteredProducts.push(productCard);
        }
    });
    return filteredProducts;
}

function writeProductCards(productCardList) {
    const productListingContainer = document.querySelector('.product-listing-container');
    productListingContainer.innerHTML = '<div class="row-cols-1 mb-3">Total products found: ' + productCardList.length + '</div>';
    productCardList.forEach(productCard => {
        productListingContainer.appendChild(productCard);
    });
}

async function handleAllergySelect() {
    let allergies = generateSelectedAllergyFilterList();
    if (allergies.length === 0) {
        return location.reload();
    }
    const filteredProducts = filterProductsByAllergies(productCardList, allergies);
    writeProductCards(filteredProducts);
}
