# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update,
         name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete,
         name='product_delete'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', views.customer_update,
         name='customer_update'),

    # Sales
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/create/', views.sale_create, name='sale_create'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:pk>/cancel/', views.sale_cancel, name='sale_cancel'),

    # Stock
    path('stock/movements/', views.stock_movements, name='stock_movements'),
    path('stock/adjustment/', views.stock_adjustment, name='stock_adjustment'),
]