from django.urls import path
from . import views
urlpatterns=[
    path('favorites/',views.favorites,name='favorite'),
    path('add-to-favorites/<int:product_id>/',views.add_items_on_favorite,name='add-to-favorite'),
    path('remove-from-favorites/<int:product_id>/<int:item_id>/',views.remove_items_from_favorites,name='remove-from-favorites'),
]