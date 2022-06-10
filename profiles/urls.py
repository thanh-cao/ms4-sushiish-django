from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history,
         name='order_history'),
    path('update_user_details/', views.update_user_details,
         name='update_user_details'),
    path('create_address/', views.create_address,
         name='create_address'),
    path('update_address/<address_id>', views.update_address,
         name='update_address'),
    path('delete_address/<address_id>', views.delete_address,
         name='delete_address'),
]
