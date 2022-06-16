from cgitb import handler
from django.urls import path
from . import views


handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact_us, name='contact_us'),
]
