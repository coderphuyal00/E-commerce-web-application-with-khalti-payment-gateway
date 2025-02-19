from django.db import models
from Cart.models import Cart,CartItem
from Cart.views import get_cart
from Accounts.models import User
from Main.models import ProductVariant
import datetime
from datetime import timezone
# Create your models here.
def default_now():
      return datetime.datetime.now()

class MailingDetails(models.Model):
    name=models.CharField(max_length=200,blank=False,null=False)
    phone=models.CharField(max_length=10,null=False,blank=False)
    email=models.EmailField()
    district=models.CharField(max_length=100,null=False,blank=False)
    city=models.CharField(max_length=100,null=False,blank=False)

class Order(models.Model):
    order_id=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_date=models.DateTimeField(default=default_now)
    shipping_address=models.ForeignKey(MailingDetails,on_delete=models.CASCADE)
    
    class Meta:
        ordering=['-order_date']

    def __str__(self):
        return f"{self.order_id} by {self.user.full_name} on {self.order_date.strftime("%Y%m%d")}"


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    item=models.ForeignKey(ProductVariant,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.product.name} in Order #{self.order.id}"

