from django.shortcuts import render, redirect
from .models import Supplier, SupplyOrder, SupplyOrderItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .forms import SupplierForm, SupplyOrderForm, SupplyOrderStatusForm
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.db import transaction
from products.models import Product


SupplyOrderItemFormSet = inlineformset_factory(
    SupplyOrder, SupplyOrderItem,
    fields=['product', 'quantity', 'unit_price'],
    extra=1, min_num=1, validate_min=True, can_delete=True
)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item_formset = kwargs.get(
            'item_formset', SupplyOrderItemFormSet()
        )

        for item_form in item_formset:
            item_form.fields['product'].queryset = Product.objects.filter(is_active=True)

        print(Product.objects.filter(is_active=True).values_list('name', flat=True))

        context['item_formset'] = item_formset
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        item_formset = SupplyOrderItemFormSet(request.POST)

        for item_form in item_formset:
            item_form.fields['product'].queryset = Product.objects.filter(is_active=True)

        if form.is_valid() and item_formset.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.created_by = request.user
                order.save()

                item_formset.instance = order
                item_formset.save()

            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form, item_formset=item_formset))

    

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