from django.shortcuts import render
from .models import CartItem
from Main.models import Product
# Create your views here.
def add_items_to_cart(request,product_id):
    item=Product.objects.get(id=product_id)
    cart_items=CartItem.objects.filter(user=request.user,product=item)
    


def Cart(request):
    item=CartItem.objects.all()

    context={
        'cart_item':item
    }
    return render(request,'cart/cart_items.html',context)
