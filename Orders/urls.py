from django.urls import path
from . import views

urlpatterns=[
    path('checkout/',views.checkout,name='checkout'),
    path('order/add/',views.add_order_items,name='create-order'),
    path('orders/',views.my_orders,name='my-order'),
    path('order/details/',views.orderSummary,name='order-summary'),
    path('order/confirmation/',views.order_confirmation,name='order-confirmation'),
    path('order/<int:order_id>/payment/',views.initiate_khalti,name='order-payment'),
]