from django.urls import path
from .views import *


urlpatterns = [
    path('inventory/movements/', MovementsListView.as_view(), name='movement_list'),
    path('inventory/movements/<int:pk>/', MovementDetailView.as_view(), name='movement_detail'),
    path('inventory/receipts/', ReceiptsListView.as_view(), name='receipt_list'),
    path('inventory/receipts/create/', ReceiptCreateView.as_view(), name='receipt_create'),
    path('inventory/receipts/<int:pk>/', ReceiptDetailView.as_view(), name='receipt_detail'),
    path('inventory/receipts/<int:pk>/post/', PostReceiptView.as_view(), name='receipt_post'),
]
