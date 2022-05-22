from django.shortcuts import render, get_object_or_404
from .models import Product, Category
# Create your views here.


def all_products(request):
    '''
    This view will show all products in the database including ability
    to filter by categories and allergies
    '''
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
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
