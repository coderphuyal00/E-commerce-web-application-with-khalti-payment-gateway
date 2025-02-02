from django.db import models
from django.contrib.auth.models import AbstractUser

 # Create your models here.
class User(AbstractUser):
    username=models.CharField(max_length=20,blank=False,null=False,unique=True)
    full_name=models.CharField(max_length=50,blank=False,null=False)
    phone=models.CharField(max_length=10)

class UserFavorites(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="favorites")
    product=models.ForeignKey('Main.Product',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.fullname+"has added this product"+self.product.name+"to favorite."