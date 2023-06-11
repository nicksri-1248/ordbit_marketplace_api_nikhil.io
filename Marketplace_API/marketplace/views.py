import uuid
import time
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import Product, Order
from .forms import ProductForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import F, ExpressionWrapper, DecimalField


class ProductListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'marketplace/product_list.html'
    context_object_name = 'products'

    def test_func(self):
        return self.request.user.is_superuser


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/product_form.html'
    success_message = 'Product created successfully!'

    def test_func(self):
        return self.request.user.is_superuser


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/product_form.html'
    success_message = 'Product updated successfully!'

    def test_func(self):
        return self.request.user.is_superuser


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Product
    template_name = 'marketplace/product_confirm_delete.html'
    success_url = '/products/'
    success_message = 'Product deleted successfully!'

    def test_func(self):
        return self.request.user.is_superuser

class ProductDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'marketplace/product_detail.html', {'product': product})

    def test_func(self):
        return self.request.user.is_superuser

class OrderListView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'marketplace/order_list.html', {'products': products})

    def post(self, request):
        order_number = int(time.time() * 1000) + random.randint(1, 1000)

        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('product')
        for product_id, quantity in zip(product_ids, quantities):
            if int(quantity) > 0:
                order = Order(product_id=product_id, quantity=quantity, order_number=order_number)
                order.user = request.user
                order.save()

        addresses = Order.objects.all().values('address').distinct()
        if addresses.exists():
            return redirect('select_address', order_number=order_number)
        else:
            return redirect('name_and_address', order_number=order_number)

class NameAndAddressView(LoginRequiredMixin, View):
    def get(self, request, order_number):
        orders = Order.objects.filter(order_number=order_number)
        return render(request, 'marketplace/name_and_address.html', {'orders': orders})

    def post(self, request, order_number):
        orders = Order.objects.filter(order_number=order_number)
        for order in orders:
            #order.name = request.POST.get('name')
            order.address = request.POST.get('address')
            order.user = request.user
            order.save()
        return redirect('delivery_date_and_time', order.order_number)
class SelectAddressView(LoginRequiredMixin, View):
    def get(self, request, order_number):
        addresses = Order.objects.values('address').annotate(num_orders=Count('id')).filter(num_orders__gt=0)
        return render(request, 'marketplace/select_address.html', {'addresses': addresses, 'order_number': order_number})

    def post(self, request, order_number):
        selected_address = request.POST.get('selected_address')
        if 'name_and_address' in request.POST:
            return redirect('name_and_address', order_number=order_number)
        else:
            orders = Order.objects.filter(order_number=order_number)
            for order in orders:
                order.address = selected_address
                order.user = request.user
                order.save()
            return redirect('delivery_date_and_time', order_number=order_number)
class DeliveryDateAndTimeView(LoginRequiredMixin, View):
    def get(self, request, order_number):
        orders = Order.objects.filter(order_number=order_number)
        return render(request, 'marketplace/delivery_date_and_time.html', {'orders': orders})

    def post(self, request, order_number):
        orders = Order.objects.filter(order_number=order_number)
        for order in orders:
            order.delivery_date = request.POST.get('delivery_date')
            order.delivery_time = request.POST.get('delivery_time')
            order.user = request.user
            order.save()
        return redirect('payment', order.order_number)

class PaymentView(LoginRequiredMixin, View):
    def get(self, request, order_number):
        orders = Order.objects.filter(order_number=order_number)
        return render(request, 'marketplace/payment.html', {'orders': orders})

    def post(self, request, order_number):
        orders = Order.objects.filter(order_number=order_number)
        for order in orders:
        #Add payment processing code here
            order.payment_status = True
            order.user = request.user
            order.save()
        return redirect('order_success', order.order_number)

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'marketplace/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.values('order_number').distinct()
        queryset = queryset.filter(user=self.request.user)
        return queryset



from django.db.models import Sum

class OrderDetailView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'marketplace/order_detail.html'
    context_object_name = 'orders'

    def get_queryset(self):
        order_number = self.kwargs['order_number']
        queryset = Order.objects.filter(order_number=order_number, user=self.request.user).annotate(
            total_product_cost=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField())
        )
        # Calculate the total cost
        total_cost = sum(order.total_product_cost for order in queryset)
        # Pass the total_cost variable to the template context
        self.total_cost = total_cost
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_number'] = self.kwargs['order_number']
        context['total_cost'] = self.total_cost  # Add total_cost to the context
        return context

class OrderSuccessView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'marketplace/order_success.html'
    context_object_name = 'orders'

    def get_queryset(self):
        order_number = self.kwargs['order_number']
        queryset = Order.objects.filter(order_number=order_number, user=self.request.user).annotate(
            total_product_cost=ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField())
        )
        # Calculate the total cost
        total_cost = sum(order.total_product_cost for order in queryset)
        # Pass the total_cost variable to the template context
        self.total_cost = total_cost
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_number'] = self.kwargs['order_number']
        context['total_cost'] = self.total_cost  # Add total_cost to the context
        return context
