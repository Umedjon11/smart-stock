from django.urls import path
from .views import (WarehouseListView,WarehouseDetailView,WarehouseCreateView,WarehouseUpdateView,WarehouseStockView,LowStockListView)

app_name = 'warehouses'

urlpatterns = [
    path('', WarehouseListView.as_view(), name='warehouse_list'),
    path('<int:pk>/', WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('create/', WarehouseCreateView.as_view(), name='warehouse_create'),
    path('<int:pk>/edit/', WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('<int:pk>/stock/', WarehouseStockView.as_view(), name='warehouse_stock'),
    path('low-stock/', LowStockListView.as_view(), name='low_stock'),
]