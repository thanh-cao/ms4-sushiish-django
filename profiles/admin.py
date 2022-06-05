from django.contrib import admin

from profiles.models import Address, UserProfile

# Register your models here.


class AddressAdminInline(admin.TabularInline):
    model = Address
    fields = ('phone_number', 'street_address1', 'street_address2',
              'town_or_city', 'postcode', 'country', 'address_type',
              'isDefault')


class UserProfileAdmin(admin.ModelAdmin):
    inlines = (AddressAdminInline,)
    list_display = ('user',)
    fields = ('user',)
    search_fields = ('user__username', 'profile_id')


admin.site.register(UserProfile, UserProfileAdmin)
