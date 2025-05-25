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

# class MailingDetails(models.Model):
#     name=models.CharField(max_length=200,blank=False,null=False)
#     phone=models.CharField(max_length=10,null=False,blank=False)
#     email=models.EmailField()
#     district=models.CharField(max_length=100,null=False,blank=False)
#     city=models.CharField(max_length=100,null=False,blank=False)

class Order(models.Model):
    order_id=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_date=models.DateTimeField(default=default_now)
    receiver_name=models.CharField(max_length=200,blank=False,null=False)
    receiver_phone=models.CharField(max_length=10,null=False,blank=False)
    receiver_email=models.EmailField()
    receiver_district=models.CharField(max_length=100,null=False,blank=False)
    receiver_city=models.CharField(max_length=100,null=False,blank=False,)
    delivery_date=models.DateTimeField()
    payment_method=models.CharField(max_length=100,blank=False,null=False)
    class Meta:
        ordering=['-order_date']
    
    def add_item(self,product,quantity,size):
        order_item=OrderItem.objects.filter(item=product,order=self,size=size)
        if order_item.exists():
            order_item.delete()
            return
        return OrderItem.objects.create(item=product,order=self,quantity=quantity,size=size)
    
    def get_ordertotal_price(self):
        order_items=OrderItem.objects.filter(order=self)
        total_price=0
        for item in order_items:
            total_price +=item.get_orderitem_price()
        return total_price
    
    def get_current_order_id(self):
        current_order_id=self.order_id
        return current_order_id
    
    def get_total_price_with_charges(self):  
        shipping_tax=10      
        total_price =self.get_ordertotal_price()+shipping_tax
        return total_price
    
    def __str__(self):
        return f"(id={self.order_id}, user='{self.user.full_name}',date='{self.order_date.strftime("%Y%m%d")}'"


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    item=models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name='products')
    size = models.CharField(max_length=50,null=False,blank=False)
    quantity=models.PositiveIntegerField()
    def __str__(self):
        return f"Order #{self.order.order_id} items"

    def get_orderitem_price(self):
        total_price=self.quantity*self.item.product.get_price()
        return total_price