from django.contrib import admin
from .models import Favorite,FavoriteItem
# Register your models here.
admin.site.register(FavoriteItem)
admin.site.register(Favorite)