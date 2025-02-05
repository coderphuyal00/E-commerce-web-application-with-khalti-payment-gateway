from django.shortcuts import render,HttpResponse
from .models import CartItem,Cart
from Main.models import ProductVariant
# Create your views here.

def add_items_to_cart(request,product_id):
    cart_item=CartItem.objects.all()
    
    if request.method=="POST":
        selected_size=request.POST.get('button_value')
    
    product_variant=ProductVariant.objects.get(id=product_id)
    productID=product_variant.product.id
    product=ProductVariant.objects.filter(id=productID).first()
    if request.user.is_authenticated:
        cart=Cart.objects.get_or_create(user=request.user)[0]
    else:
        cart=Cart.objects.get_or_create(session=request.session.session_key)[0]
    for item in cart_item:
        if item.item.product.id==product_id:
            item.is_added=True
            return HttpResponse('Item already added to bag')
        else:
            item.is_added=False
            item_on_cart=CartItem.objects.create(cart=cart,item=product,size=selected_size,is_added=True)
            # item.is_added=True

    return HttpResponse('Item added successfully')
def cart_view(request):
    
    if request.user.is_authenticated:
        cart=Cart.objects.get_or_create(user=request.user)[0]
    else:
        cart=Cart.objects.get_or_create(session=request.session.session_key)[0]
    # item=CartItem.objects.get_or_create(cart=cart)
    items=CartItem.objects.filter(cart=cart)

    context={
        'cart_items':items
    }
    return render(request,'cart/cart_items.html',context)
