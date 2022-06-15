from django.contrib import admin
from .models import ContactForm

# Register your models here.


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',)
    search_fields = ('name', 'email', 'phone',)
    readonly_fields = ('name', 'email', 'phone', 'message',)


admin.site.register(ContactForm, ContactFormAdmin)
