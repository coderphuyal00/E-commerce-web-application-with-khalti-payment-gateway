from django.db import models

# Create your models here.
class CartItem(models.Model):
    item=models.ForeignKey("Main.ProductVariant",on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        return self.item
    