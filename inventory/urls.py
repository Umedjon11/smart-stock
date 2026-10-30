from django.urls import path
from .views import *


urlpatterns = [
    path('inventory/movements/', MovementsListView.as_view(), name='movement_list'),
    path('inventory/movements/<int:pk>/', MovementDetailView.as_view(), name='movement_detail'),
    path('inventory/movements/', MovementsListView.as_view(), name='writeoff_detail'),
    path('inventory/movements/', MovementsListView.as_view(), name='movements'),
]
