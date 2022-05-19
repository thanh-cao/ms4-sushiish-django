from django.shortcuts import render
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
