from django.contrib import admin
from .models import Allergy, Product, Category

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'description', 'image')
    fields = ('name', 'price', 'category', 'description', 'image')
    search_fields = ('name', 'price', 'category', 'description')
    list_filter = ('category',)
    ordering = ('id',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Allergy)
