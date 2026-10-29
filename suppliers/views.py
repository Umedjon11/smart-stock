from django.shortcuts import render, redirect
from .models import Supplier, SupplyOrder, SupplyOrderItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import SupplierForm, SupplyOrderForm, SupplyOrderStatusForm
from django.urls import reverse_lazy, reverse



class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'


class CreateSupplierView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/create_supplier.html'
    success_url = reverse_lazy('supplier_list')

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile')
                        and user.employee_profile.position == 'manager'))
    

class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'suppliers/supplier_detail.html'
    context_object_name = 'supplier'


class UpdateSupplierView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/update_supplier.html'
    success_url = reverse_lazy('supplier_list')

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile')
                        and user.employee_profile.position == 'manager'))


class DeleteSupplierView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Supplier
    success_url = reverse_lazy('supplier_list')

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile')
                        and user.employee_profile.position == 'manager'))


class SupplyOrderListView(LoginRequiredMixin, ListView):
    model = SupplyOrder
    template_name = 'suppliers/order_list.html'
    context_object_name = 'orders'
    ordering = ['-order_date']


class CreateSupplyOrderView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SupplyOrder
    form_class = SupplyOrderForm
    template_name = 'suppliers/create_order.html'
    success_url = reverse_lazy('order_list')

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile') 
                        and user.employee_profile.position == 'manager'))

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SupplyOrderDetailView(LoginRequiredMixin, DetailView):
    model = SupplyOrder
    template_name = 'suppliers/order_detail.html'
    context_object_name = 'order'


class UpdateSupplyOrderStatusView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SupplyOrder
    form_class = SupplyOrderStatusForm
    template_name = 'suppliers/update_order_status.html'

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile') 
                and user.employee_profile.position in ['manager', 'warehouse_worker', ]))

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})