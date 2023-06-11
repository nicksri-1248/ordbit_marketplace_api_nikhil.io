from django.urls import path
from .views import (
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductDetailView,
    OrderListView, NameAndAddressView, SelectAddressView, DeliveryDateAndTimeView, PaymentView, OrderHistoryView, OrderDetailView, OrderSuccessView
)

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('order/', OrderListView.as_view(), name='order_list'),
    path('orders/', OrderHistoryView.as_view(), name='order_history'),
    # path('orderlist/', OrderHistoryView.as_view(), name='order_list'),
    path('order/<int:order_number>/', OrderDetailView.as_view(), name='order_detail'),
    path('name-and-address/<int:order_number>/', NameAndAddressView.as_view(), name='name_and_address'),
    path('select-address/<int:order_number>/', SelectAddressView.as_view(), name='select_address'),
    path('delivery-date-and-time/<int:order_number>/', DeliveryDateAndTimeView.as_view(), name='delivery_date_and_time'),
    path('payment/<int:order_number>/', PaymentView.as_view(), name='payment'),
    path('ordercc/<int:order_number>/', OrderSuccessView.as_view(), name='order_success'),
]