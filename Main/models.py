from django.db import models
import os
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20,blank=False,null=False)

    def __str__(self):
        return self.name
class Size(models.Model):
    eu_size=models.CharField(max_length=20,blank=False,null=False)
    us_size=models.CharField(max_length=20,blank=False,null=False)
    uk_size=models.CharField(max_length=20,blank=False,null=False)

    def __str__(self):
        return f"EUR : "+self.eu_size+" "+"US : "+self.us_size+" "+"UK : "+self.uk_size
class Product(models.Model):
    name=models.CharField(max_length=20,blank=False,null=False)
    description=models.TextField()
    price=models.FloatField() 
    sale_price=models.FloatField() 
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    added_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

def upload_to_product_img(instance, filename):
    """
    Defines the upload path for product images.
    """

    filename = os.path.basename(filename)
    return os.path.join("product_imgs", filename)


class ProductImage(models.Model):
    image=models.ImageField(upload_to=upload_to_product_img)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

class ProductVariant(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color= models.TextField(max_length=100,blank=False,null=False)
    size= models.ManyToManyField(Size,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    def __str__(self):
        return f"Variation of "+self.product.name

