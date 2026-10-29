
from django.urls import path
from .views import ProductList,ProductDetail,ProductCreateView

app_name = 'products'

urlpatterns=[
    path('', ProductList.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
]