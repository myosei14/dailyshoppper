from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<slug>/', views.update_cart, name='update-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('create-payment-intent/', views.create_payment, name='create_payment'),
    path('order-status', views.order_status, name='order_status'),

]