from django.urls import path
from payments import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-checkout-session/', views.create_checkout_session, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel.html/', views.cancel, name='cancel'),
]