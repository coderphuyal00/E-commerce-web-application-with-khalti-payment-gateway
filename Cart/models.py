from django.db import models
from django.urls import reverse
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey('Accounts.User',on_delete=models.CASCADE,default=None,blank=True,null=True)
    session=models.CharField(max_length=50,null=True,blank=True,default=None)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    item=models.ForeignKey("Main.ProductVariant",on_delete=models.CASCADE,null=True)
    size = models.CharField(max_length=50,null=False,blank=False)
    is_added=models.BooleanField(blank=False,null=False)
    def __str__(self):
        return self.item.product.name
    
    def get_absoulte_url(self):
        return reverse("cart",args=[str(self.id)])