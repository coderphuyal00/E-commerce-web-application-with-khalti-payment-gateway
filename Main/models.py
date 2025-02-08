from django.db import models
import os
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20,blank=False,null=False)

    def __str__(self):
        return self.name
class Size(models.Model):
    size = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.size

class Product(models.Model):
    name=models.CharField(max_length=20,blank=False,null=False)
    description=models.TextField()
    price=models.FloatField() 
    sale_price=models.FloatField(null=True,blank=True) 
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    added_on=models.DateTimeField(auto_now_add=True)
    sku=models.CharField(max_length=50,null=False,blank=False)

    def get_price(self):
        if self.sale_price:
            return self.sale_price
        return self.price
    def __str__(self):
        return self.name

def upload_to_product_img(instance, filename):
    """
    Defines the upload path for product images.
    """

    filename = os.path.basename(filename)
    return os.path.join("media/product_imgs", filename)


class ProductImage(models.Model):
    image=models.ImageField(upload_to=upload_to_product_img)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

class ProductVariant(models.Model):
#     sizes = [
#     ("35/5/34.5","EUR : 35.0 / US : 5.0 / UK : 34.5"),
#     ("35.5/5.5/35","EUR : 35.5 / US : 5.5 / UK : 35.0"),
#     ("36/6/35.5","EUR : 36 / US : 6 / UK : 35.5"),
#     ("37/6.5/36.5","EUR : 37 / US : 6.5 / UK : 36.5"),
#     ("37.5/7/37","EUR : 37.5 / US : 7 / UK : 37"),
#     ("38/7.5/37.5","EUR : 38 / US : 7.5 / UK : 37.5"),
#     ("38.5/8/38","EUR : 38.5 / US : 8 / UK : 38"),
#     ("39/8.5/38.5","EUR : 39 / US : 8.5 / UK : 38.5"),
#     ("39.5/9/39","EUR : 39.5 / US : 9 / UK : 39"),
#     ("40/9.5/39.5","EUR : 40 / US : 9.5 / UK : 39.5")
# ]
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="variants")
    color= models.TextField(max_length=100,blank=False,null=False)
    size= models.ManyToManyField(Size)
    quantity=models.IntegerField(null=False,blank=False,default=1)
    def __str__(self):
        return f"Variation of "+self.product.name
