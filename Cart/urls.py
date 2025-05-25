from django.urls import path
from . import views
urlpatterns=[
    path('cart-items/',views.cart_view,name='cart-view'),
    path('test-items/',views.get_total_items,name='test-view'),
    path('add-to-cart/<int:product_id>/',views.add_items_to_cart,name='add-to-cart'),
    path('update-cart/<int:cart_item_id>/',views.update_cart,name='update-cart'),
    path('remove-from-cart/<int:product_id>/<int:cart_item_id>/',views.remove_from_cart,name='remove-from-cart'),
    path('total_items/',views.get_total_items,name='total_items_on_cart'),
]