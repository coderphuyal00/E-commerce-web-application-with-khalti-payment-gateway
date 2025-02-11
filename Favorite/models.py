from django.db import models
from Accounts.models import User
from Main.models import ProductVariant
# Create your models here.

class Favorite(models.Model):   
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def add_item(self,product):
        favorite_items=FavoriteItem.objects.filter(item=product,favorite=self)
    
        if favorite_items.exists():
            favorite_items=favorite_items.first()
            return
        return FavoriteItem.objects.get_or_create(item=product,favorite=self)

    def __str__(self):
        return f"{self.user} favorite's."

class FavoriteItem(models.Model):
     favorite=models.ForeignKey(Favorite,on_delete=models.CASCADE)
     item=models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
     

     def __str__(self):
        return f"{self.favorite.user} has listed {self.item.product.name} on favorites."