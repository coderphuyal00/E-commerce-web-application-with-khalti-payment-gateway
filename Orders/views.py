from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from Orders.models import Order,OrderItem,MailingDetails
from Main.models import Product,ProductVariant
from Cart.views import get_cart
from Cart.models import CartItem,Cart
import datetime
from datetime import timezone
def get_checkout_user(request):
    if  request.user.is_authenticated:
        user, created=Order.objects.get_or_create(user=request.user)
    else:
        return redirect('account_login')
    return user
# Create your views here.
def checkout(request):
    cart=Cart.objects.get(user=request.user)
    # get cart items of the following cart
    cart_items=cart.cartitem_set.all()
    context={
        'items':cart_items,
        'cart':cart
    }
    return  render(request,'orders/checkout.html',context)

def add_mailingaddress(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('number')
        district=request.POST.get('district')
        city=request.POST.get('city')
        order_address=MailingDetails.objects.create(name=name,phone=phone,email=email,district=district,city=city)
        return  order_address

class OrderIDGenerator:
    def __init__(self):
        self.counter=0
        self.current_date=datetime.datetime.now().strftime("%Y%m%d")

    def generator_order_id(self):
        today=datetime.datetime.now().strftime("%Y%m%d")
        if today!=self.current_date:
            self.counter=0
            self.current_date=today
        self.counter += 1
        return f"ORD-{self.current_date}-{self.counter:04d}"

def create_order(request):
    user=request.user
    address=add_mailingaddress(request)
    order_id_generator=OrderIDGenerator()
    order_id=order_id_generator.generator_order_id()
    order=Order.objects.create(order_id=order_id,user=user,shipping_address=address)
    return order
def get_cart_items(request):
    # get cart 
    cart=Cart.objects.get(user=request.user)
    # get cart items of the following cart
    cart_items=cart.cartitems_set.all()

def add_order_items(request):
    # order
    order=create_order(request)
    # item
    cart=Cart.objects.get(user=request.user)
    items=cart.cartitem_set.all()
    product_id=0
    for item in items:
        product_id=item.item.product.id
        product=ProductVariant.objects.filter(id=product_id).first()
        order_item=OrderItem.objects.get_or_create(order=order,item=product)
    # product_variant=ProductVariant.objects.get(id=product_id)
    # productID=product_variant.product.id
    return HttpResponse("Order Created!!")