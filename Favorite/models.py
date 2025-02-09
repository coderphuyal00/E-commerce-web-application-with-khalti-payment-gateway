from django.db import models
from Accounts.models import User
from Main.models import ProductVariant
# Create your models here.

class Favorite(models.Model):
    item=models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.full_name} added {self.item.product.name} on favorites."