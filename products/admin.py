from django.contrib import admin
from .models import Allergy, Product, Category

# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Allergy)
