from django.urls import path
from .views import *


urlpatterns = [
    path('transfers/', TranfersListView.as_view(), name='transfer_list'),
    path('transfers/create/', TranferCreateView.as_view(), name='transfer_create'),
    path('transfers/<int:pk>/', TranferDetailView.as_view(), name='transfer_detail'),
    path('transfers/<int:pk>/post/', PostTranferView.as_view(), name='transfer_post')
]
