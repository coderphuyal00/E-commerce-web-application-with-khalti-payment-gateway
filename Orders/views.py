from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from Orders.models import Order,OrderItem,MailingDetails
from Main.models import Product,ProductVariant
from Cart.views import get_cart
from Cart.models import CartItem,Cart
from datetime import datetime,timedelta
import threading
import requests
import json
import os
from dotenv import load_dotenv
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

def delivery_date_generator(self):
    today=self
def create_order(request):
    user=request.user
    address=add_mailingaddress(request)
    order_id=order_id_generator.generate_order_id()
    delivery_date=datetime.now()+timedelta(days=5)
    order=Order.objects.create(order_id=order_id,user=user,shipping_address=address,delivery_date=delivery_date)
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
    order_id=order.id
    if request.method=="POST":
        payment_method=request.POST.get('payment_method')
        if payment_method=='khalti':
            return initiate_khalti(request,order_id)
        else:
            return redirect('order-summary')
    else:
        return HttpResponse('Please select the payment method.') 
          

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

def orderSummary(request):
    order=Order.objects.filter(user=request.user).first()

    context={
        'order':order
    }
    return render(request,'orders/order_summary.html',context)
def order_confirmation(request):
    return render(request,'orders/transaction_completed.html')
# Payment Gateway Integration
def initiate_khalti(request,order_id):
    order=Order.objects.get(id=order_id)
    amount=int(order.get_total_price_with_charges())
    customer_name=order.shipping_address.name
    customer_email=order.shipping_address.email
    customer_phone=order.shipping_address.phone
    load_dotenv()
    url = "https://dev.khalti.com/api/v2/epayment/initiate/"
    payload = json.dumps({
        "return_url": "https://www.youtube.com",
        "website_url": "http://127.0.0.1:8000/",
        "amount": amount,
        "purchase_order_id": order.order_id,
        "purchase_order_name": 'test' ,
        "customer_info": {
        "name": customer_name,
        "email": customer_email,
        "phone": customer_phone
        }
    })
    # print(os.getenv("LIVE_SECRET_KEY"))
    headers = {
        'Authorization': f"{os.getenv("LIVE_SECRET_KEY")}",
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    data=response.json()
    payment_url=data["payment_url"]
    return HttpResponseRedirect(payment_url)
