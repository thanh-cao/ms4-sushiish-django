from django.urls import path
from . import views


urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('stripe/keys/', views.get_stripe_keys, name='get_stripe_keys'),
]
