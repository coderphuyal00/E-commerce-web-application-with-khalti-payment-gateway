from django.db import models
from Cart.models import Cart,CartItem
from Cart.views import get_cart
# Create your models here.
class Order(models.Model):
    item=CartItem.objects.get()