from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Warehouses, Stock

class WarehouseListView(ListView):
    model = Warehouses
    template_name = 'nozim/warehouse_list.html'
    context_object_name = 'warehouses'

class WarehouseDetailView(DetailView):
    model = Warehouses
    template_name = 'nozim/warehouse_detail.html'
    context_object_name = 'warehouse'

class WarehouseCreateView(LoginRequiredMixin, CreateView):
    model = Warehouses
    fields = ['name', 'address', 'is_active']
    template_name = 'nozim/warehouse_form.html'
    success_url = reverse_lazy('warehouses:warehouse_list')
    login_url = '/admin/login/'

class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    model = Warehouses
    fields = ['name', 'address', 'is_active']
    template_name = 'nozim/warehouse_form.html'
    success_url = reverse_lazy('warehouses:warehouse_list')
    login_url = '/admin/login/'

class WarehouseStockView(ListView):
    model = Stock
    template_name = 'nozim/warehouse_stock.html'
    context_object_name = 'stocks'

    def get_queryset(self):
        self.warehouse = get_object_or_404(Warehouses, pk=self.kwargs['pk'])
        return Stock.objects.filter(warehouse=self.warehouse).select_related('product', 'product__category', 'product__unit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouse'] = self.warehouse
        return context

class LowStockListView(ListView):
    model = Stock
    template_name = 'nozim/low_stock.html'
    context_object_name = 'low_stocks'

    def get_queryset(self):
        return Stock.objects.filter(
            quantity__lte=F('product__min_stock_level'),
            product__is_active=True
        ).select_related('warehouse', 'product', 'product__unit')

