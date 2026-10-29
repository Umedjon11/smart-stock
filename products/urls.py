
from django.urls import path
from .views import ProductList,ProductDetail,ProductCreateView,ProductUpdateView,ProductArchiveView,CategoryCreateView,CategoryListView

app_name = 'products'

urlpatterns=[
    path('', ProductList.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),     
    path('<int:pk>/archive/', ProductArchiveView.as_view(), name='product_archive'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),

]