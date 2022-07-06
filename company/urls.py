from django.urls import path
from . import views

urlpatterns = [
    path("company/", views.company, name="company"),
    path("orders/", views.orders, name="orders"),
    path("products/", views.products, name="products")
]