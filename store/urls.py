#store/urls.py
from django.urls import path
from . import views
from .views import ProductDetailUpdateView

urlpatterns = [
    path('', views.api_root, name='api-root'),

    # Public Products
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailUpdateView.as_view(), name='product-detail'),
    # Public Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),


    # Admin APIs
    path('admin/products/', views.ProductList.as_view(), name='admin-products'),
    path('admin/products/low-stock/', views.LowStockProductsView.as_view(), name='low-stock-products'),
    path('admin/categories/', views.CategoryListView.as_view(), name='admin-categories'),
    path('admin/orders/', views.OrderListView.as_view(), name='admin-orders'),  # <-- Add this
    path('admin/orders/recent/', views.RecentOrdersView.as_view(), name='recent-orders'),
    path('admin/reports/', views.ReportListView.as_view(), name='admin-reports'),
    path('admin/stats/', views.AdminStatsView.as_view(), name='admin-stats'),
    path('admin/banners/', views.BannerListView.as_view(), name='admin-banners'),  # <-- Add this
]
