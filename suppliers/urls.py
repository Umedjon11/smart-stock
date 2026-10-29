from django.urls import path
from .views import (SupplierListView, CreateSupplierView, SupplierDetailView, UpdateSupplierView,
                DeleteSupplierView, SupplyOrderListView, CreateSupplyOrderView, SupplyOrderDetailView,
                UpdateSupplyOrderStatusView   )

urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('create-supplier/', CreateSupplierView.as_view(), name='create_supplier'),
    path('supplier-detail/<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('update-supplier/<int:pk>/', UpdateSupplierView.as_view(), name='update_supplier'),
    path('delete-supplier/<int:pk>/', DeleteSupplierView.as_view(), name='delete_supplier'),
    # order=========
    path('orders/', SupplyOrderListView.as_view(), name='order_list'),
    path('create-order/', CreateSupplyOrderView.as_view(), name='create_order'),
    path('orders-detail/<int:pk>/', SupplyOrderDetailView.as_view(), name='order_detail'),
    path('order-status/<int:pk>/', UpdateSupplyOrderStatusView.as_view(), name='update_order_status'),
    
]