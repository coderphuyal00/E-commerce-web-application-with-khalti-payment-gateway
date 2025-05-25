from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from Orders.models import Order,OrderItem
from Main.models import Product,ProductVariant
from Cart.views import get_cart
from Cart.models import CartItem,Cart
from datetime import datetime,timedelta
import threading
import requests
import json
import os
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv
def get_checkout_user(request):
    if  request.user.is_authenticated:
        user, created=Order.objects.get_or_create(user=request.user)
    else:
        return redirect('account_login')
    return user
# Create your views here.

def checkout(request):
    district_list=json_data()
    if request.user.is_authenticated:
        cart=Cart.objects.get(user=request.user)
    # get cart items of the following cart
        cart_items=cart.cartitem_set.all()
    else:
        return redirect('account_login')
    context={
        'items':cart_items,
        'cart':cart,
        'data':district_list
    }
    return  render(request,'orders/checkout.html',context)

# def add_mailingaddress(request):
#     if request.method=="POST":
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         phone=request.POST.get('number')
#         district=request.POST.get('district')
#         city=request.POST.get('city')
#         order_address=MailingDetails.objects.get_or_create(name=name,phone=phone,email=email,district=district,city=city)
#         return  order_address


class OrderIDGenerator:
    def __init__(self):
        self.counter = 0
        self.current_date = None
        self.lock = threading.Lock()

    def generate_order_id(self):
        with self.lock:
            # Get current date
            today = datetime.now().strftime("%Y%m%d")
            last_order=Order.objects.all().first()
            last_order_counter=int(last_order.order_id)
            last_order_date=last_order_counter//10000
            last_counter=last_order_counter % 100
            # Reset counter if date changed            
            # if self.current_date != today:
            #     self.counter = 0
            #     self.current_date = today
            
            # Increment counter
            if last_order and last_order_date==today:
                self.counter=last_counter+1
            else:
                # self.current_date = today
                self.counter+=1
            # self.counter += 1
            self.current_date = today
            # Generate order ID in format ORD-YYYYMMDD-XXXX
            return f"{self.current_date}{self.counter:04d}"

order_id_generator=OrderIDGenerator()


def delivery_date_generator(self):
    today=self


# creates order
def create_order(request):
    user=request.user    
    order_id=order_id_generator.generate_order_id()
    delivery_date=datetime.now()+timedelta(days=5)
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('number')
        district=request.POST.get('district')
        city=request.POST.get('city')
        order, created=Order.objects.get_or_create(
        order_id=order_id,
        defaults={
                'user': user,
                'receiver_name': name,
                'receiver_email': email,
                'receiver_phone': phone,
                'receiver_district': district,
                'receiver_city': city,
                'delivery_date': delivery_date,
            })
    
    # redirect('payment')
    return order_id


def send_welcome_email(email):
    send_mail(
        subject='Your Order is placed.',
        message='Please receive the order on specific date',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

def get_cart_items(request):
    # get cart 
    cart=Cart.objects.get(user=request.user)
    # get cart items of the following cart
    cart_items=cart.cartitems_set.all()

# adds items of the order to the order 
def add_order_items(request):
    # order
    order_id=create_order(request)  
    request.session['order_id'] = order_id
    order=Order.objects.get(order_id=order_id)
    # item
    cart=Cart.objects.get(user=request.user)
    items=cart.cartitem_set.all()
    product_id=0
    for cart_item in items:
        product_id=cart_item.item.product.id
        product=ProductVariant.objects.filter(id=product_id).first()
        quantity=cart_item.quantity
        size=cart_item.size
        order.add_item(product,quantity,size)    
    # product_variant=ProductVariant.objects.get(id=product_id)
    # productID=product_variant.product.id
    order_id=order.id
    return redirect('payment')


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

def payment_details(request):
    order_id=request.session.get('order_id')
    url=initiate_khalti(request,order_id)
    order=Order.objects.get(order_id=order_id)
    # order_items=OrderItem.objects.get(order=order)
    items=order.items.all()
    context={
        'url':url,
        'order_items':items,
        'order':order
    }

    return render(request,'orders/payment_details.html',context)

def payment(request):
    order_id=request.session.get('order_id')
    order=get_object_or_404(Order, order_id=order_id)
    if request.method=="POST":
        paymentMethod=request.POST.get('payment_method')
        print(paymentMethod)
        if paymentMethod == '2':
            pay_method = "Cash on Delivery"            
        else:
             pay_method = None
        print(pay_method)    
        if pay_method:
            order.payment_method = pay_method
            order.save()
        else:
            print("Warning: payment method not set properly.")
    # order.payment_method=pay_method
    # order.save()
    email=order.email
    send_welcome_email(email)
    return redirect('order-summary')    
    
    
# Payment Gateway Integration
def initiate_khalti(request,order_id):   
    # order=get_object_or_404(Order, order_id=order_id)
    order=Order.objects.get(order_id=order_id)
    order.payment_method='Khalti'
    order.save()
    # print(order)
    cart=Cart.objects.get(user=request.user)
    # print(order)
    amount=cart.get_total_price_with_charges()
    customer_name=order.receiver_name
    customer_email=order.receiver_email
    customer_phone=order.receiver_phone
    load_dotenv()
    url = "https://dev.khalti.com/api/v2/epayment/initiate/"
    payload = json.dumps({
        "return_url": "http://127.0.0.1:8000/order/details/",
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
    print(payment_url)
    # redirect(payment_url)
    # if payment_url:
    #     print(payment_url)
    #     return redirect(payment_url)
    # else:
    #     return HttpResponse("Payment URL not found", status=400)
    return payment_url

def json_data():
    # Construct path to JSON file
    json_path = os.path.join('district_list.json')
    
    # Open and load JSON data
    with open(json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)  # data is now a Python dict or list
    
    # Pass data to template context
    return data