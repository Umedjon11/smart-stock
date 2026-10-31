from django.urls import path
from .views import Dashboard, StockReportView, MovementReportView, LowStockReportView

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('stock/', StockReportView.as_view(), name='stock_report'),
    path('movement/', MovementReportView.as_view(), name='movement_report'),
    path('low-stock/', LowStockReportView.as_view(), name='low_stock_report')

]