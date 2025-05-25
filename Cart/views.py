from django.shortcuts import render,HttpResponse,redirect
from .models import CartItem,Cart
from Main.models import ProductVariant
# Create your views here.
def get_cart(request):
    if request.user.is_authenticated:
        cart, created =Cart.objects.get_or_create(user=request.user)
    else:
        session_key=request.session.session_key
        if not session_key:
            request.session.create()

            session_key=request.session.session_key

        try:
                cart=Cart.objects.get(session=session_key)

        except Cart.DoesNotExist:
                cart=Cart.objects.create(session=session_key)
                
    return cart  


def associate_cart_with_user(request, user):  # Associate cart on login
    """
    Associates the anonymous cart (if any) with the user after login.
    """
    session_key = request.session.session_key
    if session_key:
        try:
            anonymous_cart = Cart.objects.get(session=session_key)
            anonymous_cart.user = user
            anonymous_cart.session = None  # Remove the session key
            anonymous_cart.save()
        except Cart.DoesNotExist:
            pass
 
def add_items_to_cart(request,product_id):
    # cart_item=CartItem.objects.all()
    if request.method=="POST":
        selected_size=request.POST.get('button_value')
    
    product_variant=ProductVariant.objects.get(id=product_id)
    productID=product_variant.product.id
    product=ProductVariant.objects.filter(id=productID).first()
    cart1=get_cart(request)    
    quantity=1
    cart1.add_item(product,quantity,selected_size)
    count_cart_items(request)
    return redirect('cart-view')

def remove_from_cart(request,product_id,cart_item_id):
    product_variant=ProductVariant.objects.get(id=product_id)
    productID=product_variant.product.id
    product=ProductVariant.objects.filter(id=productID).first()
    if request.user.is_authenticated:
        cart=Cart.objects.get_or_create(user=request.user)[0]
    else:
        cart=Cart.objects.get_or_create(session=request.session.session_key)[0]

    cart_item=CartItem.objects.get(id=cart_item_id,item=product).delete()
    # cart_item.delete()
    return redirect("cart-view")

def update_cart(request,cart_item_id):
     cart_item=CartItem.objects.get(id=cart_item_id)
     cart=cart_item.cart
     if request.method=="POST":
        quantity=request.POST.get('quantity')
     cart_item.quantity=quantity 
     cart_item.save()      
     cart.save()
     return redirect("cart-view")     
def cart_view(request):
    cart=get_cart(request)
    # item=CartItem.objects.get_or_create(cart=cart)
    # items=CartItem.objects.filter(cart=cart)

    items = cart.cartitem_set.all()
    context={
        'cart_items':items,
        'cart':cart
    }
    return render(request,'cart/cart_items.html',context)

def count_cart_items(request):
   cart=get_cart(request) 
   total_items=cart.cartitem_set.count()
   request.session['total_items']=total_items

   return render(request,'header.html',{'total_items':total_items})

#    return response

def get_total_items(request):
    # count_cart_items(request)
    total_items=request.session.get('total_items')
    
    
    return render(request,'header.html',{'total_items':total_items})