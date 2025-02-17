from django.shortcuts import render,redirect
from Orders.models import Order,OrderItem,MailingAddress
from Main.models import Product,ProductVariant
def get_checkout_user(request):
    if  request.user.is_authenticated:
        user, created=Order.objects.get_or_create(user=request.user)
    else:
        return redirect('account_login')
# Create your views here.
def checkout(request):
    return  render(request,'orders/checkout.html')

def add_mailingaddress(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        district=request.POST.get('phone')
        city=request.POST.get('phone')
    order_address=MailingAddress.objects.create(name=name,phone=phone,email=email,district=district,city=city)
    return  order_address

def order_items(request,product_id):
    product_variant=ProductVariant.objects.get(id=product_id)
    product=product_variant.product.id
    item=ProductVariant.objects.filter(product=product).first()