from django.urls import path
from . import views
urlpatterns=[
    path('cart-items/',views.Cart,name='cart')
]