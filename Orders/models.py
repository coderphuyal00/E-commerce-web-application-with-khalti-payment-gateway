from django.db import models
from Cart.models import Cart,CartItem
from Cart.views import get_cart
from Accounts.models import User
from Main.models import ProductVariant
import datetime
from datetime import timezone,datetime,timedelta
# Create your models here.
def default_now():
      return datetime.now()

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
    delivery_date=models.DateTimeField()
    payment_method=models.CharField(max_length=100,blank=False,null=False)
    class Meta:
        ordering=['-order_date']
    
    
    def get_ordertotal_price(self):
        order_items=OrderItem.objects.filter(order=self)
        total_price=0
        for item in order_items:
            total_price +=item.get_orderitem_price()
        return total_price
    
    def get_total_price_with_charges(self):
        shipping_charge=1.25
        tax=10
        total_price=0
        order=Order.objects.get(id=self.id)     
        total_price +=order.get_ordertotal_price()+shipping_charge+tax
        return total_price
    
    def __str__(self):
        return f"{self.order_id} by {self.user.full_name} on {self.order_date.strftime("%Y%m%d")}"


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    item=models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name='products')
    size = models.CharField(max_length=50,null=False,blank=False)
    quantity=models.PositiveIntegerField()
    def __str__(self):
        return f"{self.item.product.name} in Order #{self.order.id}"

    def get_orderitem_price(self):
        total_price=self.quantity*self.item.product.get_price()
        return total_price