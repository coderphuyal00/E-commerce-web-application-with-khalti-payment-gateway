from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey('Accounts.User',on_delete=models.CASCADE,blank=True,null=True)
    session=models.CharField(max_length=50,null=True,blank=True,default=None)
    def add_item(self,product,quantity,size):
        cart_item=CartItem.objects.filter(item=product,cart=self,size=size)
        if cart_item.exists():
            cart_item=cart_item.first()
            cart_item.quantity=cart_item.quantity+quantity
            cart_item.save()
            return
        return CartItem.objects.create(item=product,cart=self,quantity=quantity,size=size)
    
    def remove_item(self,product):

        return CartItem.objects.get(item=product,cart=self).delete()
    def get_total_price(self):
        cart_items=self.cartitem_set.all()
        total_price=0
        for item in cart_items:
            total_price += item.get_item_price()
        return total_price

    def __str__(self):
        if self.user:
            return f"{self.user.email}'s cart"
        else:
            return f"{self.session}'s cart"
        

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    item=models.ForeignKey("Main.ProductVariant",on_delete=models.CASCADE,null=True)
    size = models.CharField(max_length=50,null=False,blank=False)
    quantity=models.PositiveIntegerField()
    def __str__(self):
        return self.item.product.name
    
    def get_item_price(self):                 
        total_price=self.quantity*self.item.product.get_price()
        
        return total_price           
                
    def get_absoulte_url(self):
        return reverse("cart",args=[str(self.id)])