from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from .models import Product, Category
# Create your views here.


def all_products(request):
    '''
    This view will show all products in the database including ability
    to filter by categories and allergies
    '''
    products = Product.objects.all()
    categories = Category.objects.all()
    search_query = None

    if request.GET:
        if 'search' in request.GET:
            search_query = request.GET['search']
            if not search_query:
                return redirect(reverse('products'))

            queries = Q(name__icontains=search_query) | Q(
                description__icontains=search_query)
            products = products.filter(queries)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    '''
    This view will show details of a product
    '''
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)
