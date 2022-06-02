from django.urls import path
from . import views
from .webhook import stripe_webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('update_order_type/', views.update_order_type,
         name='update_order_type'),
    path('update_order_info/', views.update_order_info,
         name='update_order_info'),
    path('stripe/keys/', views.get_stripe_keys, name='get_stripe_keys'),
    path('success/<order_number>', views.checkout_success,
         name='checkout_success'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
]
