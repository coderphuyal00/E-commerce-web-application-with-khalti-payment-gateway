from django.urls import path
from . import views
urlpatterns=[
    path('cart-items/',views.cart_view,name='cart-view'),
    path('add-to-cart/<int:product_id>/',views.add_items_to_cart,name='add-to-cart'),
]