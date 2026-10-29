
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Product


class ProductList(ListView):
    model = Product
    template_name = 'nozim/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).select_related('category', 'unit')


class ProductDetail(DetailView):
    model = Product
    template_name = 'nozim/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True
        ).select_related('category', 'unit')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product

    fields = [
        'sku',
        'name',
        'category',
        'unit',
        'description',
        'min_stock_level',
        'image',
        'is_active'
    ]

    template_name='nozim/product_form.html'
    success_url = reverse_lazy('products:product_list')
    login_url = '/admin/login/'
