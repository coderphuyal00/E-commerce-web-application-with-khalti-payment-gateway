from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from Orders.models import Order,OrderItem,MailingDetails
from Main.models import Product,ProductVariant
from Cart.views import get_cart
from Cart.models import CartItem,Cart
from datetime import datetime
import threading
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
        self.counter = 0
        self.current_date = None
        self.lock = threading.Lock()

    def generate_order_id(self):
        with self.lock:
            # Get current date
            today = datetime.now().strftime("%Y%m%d")
            
            # Reset counter if date changed
            if self.current_date != today:
                self.counter = 0
                self.current_date = today
            
            # Increment counter
            self.counter += 1
            
            # Generate order ID in format ORD-YYYYMMDD-XXXX
            return f"{self.current_date}{self.counter:04d}"

order_id_generator=OrderIDGenerator()
def create_order(request):
    user=request.user
    address=add_mailingaddress(request)
    order_id=order_id_generator.generate_order_id()
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
        quantity=item.quantity
        size=item.size
        order_item=OrderItem.objects.get_or_create(order=order,item=product,quantity=quantity,size=size)
    # product_variant=ProductVariant.objects.get(id=product_id)
    # productID=product_variant.product.id
    return HttpResponse("Order Created!!")

def my_orders(request):
    orders=Order.objects.filter(user=request.user)
    order_items=OrderItem.objects.filter(order__in=orders)
    items=Order.objects.prefetch_related('items').all()
    # for order in orders:
    #     order_id=Order.objects.get(id=order.id)
    #     items=order_id.orderitem_set.all()
    context={
        'orders':orders,
        'order_items':items,
        # 'items':items
    }
    return render(request,'orders/my_order.html',context)
# def my_orders(request):
#     order=Order.objects.filter(user=request.user).first()
#     order_items=order.orderitem_set.all()

#     context={
#         'order':order,
#         'order_items':order_items
#     }
#     return render(request,'orders/my_orders.html',context)

def orderSummary(request,item_id):
    order=Order.objects.filter(user=request.user)