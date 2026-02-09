from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('filter/', views.filter_products, name='filter_products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
