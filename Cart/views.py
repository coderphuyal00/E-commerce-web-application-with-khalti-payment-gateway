from django.shortcuts import render,HttpResponse
from .models import CartItem,Cart
from Main.models import ProductVariant
# Create your views here.

def add_items_to_cart(request,product_id):
    product_variant=ProductVariant.objects.get(id=product_id)
    productID=product_variant.product.id
    product=ProductVariant.objects.filter(id=productID).first()
    if request.user.is_authenticated:
        cart=Cart.objects.get_or_create(user=request.user)[0]
    else:
        cart=Cart.objects.get_or_create(session=request.session.session_key)[0]

    item_on_cart=CartItem.objects.create(cart=cart,item=product)

    return HttpResponse('Item added successfully')
def cart_view(request):
    item=CartItem.objects.all()

    context={
        'cart_items':item
    }
    return render(request,'cart/cart_items.html',context)
