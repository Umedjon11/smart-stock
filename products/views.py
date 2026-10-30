
from django.views.generic import ListView, DetailView, CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Product,Category


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

    fields = ['sku','name','category','unit','description','min_stock_level','image','is_active']

    template_name='nozim/product_form.html'
    success_url = reverse_lazy('products:product_list')
    login_url = '/admin/login/'




class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['sku', 'name', 'category', 'unit', 'description', 'min_stock_level', 'image', 'is_active']
    template_name = 'nozim/product_form.html'
    success_url = reverse_lazy('products:product_list')
    login_url = '/admin/login/'

class ProductArchiveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_active = False
        product.save()
        return redirect('products:product_list')



class CategoryListView(ListView):
    model = Category
    template_name = 'nozim/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']  
    template_name = 'nozim/category_form.html'
    success_url = reverse_lazy('products:category_list')
    login_url = '/admin/login/'





