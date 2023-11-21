from re import template
from django.urls import path
from . import views


urlpatterns = [
    # path('', views.Authz.as_view()),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.login_customer, name='login'),
    path('logout/', views.logout_customer, name='logout'),
    path('account/', views.Account.as_view(), name='account'),
]

