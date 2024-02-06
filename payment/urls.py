from django.urls import path
from . import views

urlpatterns = [
    path('category', views.shop, name="category"),
    path('product_detail/<slug>', views.product_detail, name='product_detail'),
]