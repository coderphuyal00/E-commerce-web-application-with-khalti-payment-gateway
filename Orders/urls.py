from django.urls import path
from . import views

urlpatterns=[
    path('checkout/',views.checkout,name='checkout'),
    path('order/add/',views.add_order_items,name='create-order'),
]