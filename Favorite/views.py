from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Main.models import ProductVariant
from .models import Favorite
# Create your views here.
def favorites(request):
    product=Favorite.objects.get(user=request.user)
    if request.user==product.user:
        products=Favorite.objects.all()
    context={
        "product":products
     }
    return render(request,"favorites/favorite_list.html",context)
        

@login_required
def add_items_on_favorite(request,product_id):
    product=ProductVariant.objects.get(id=product_id)
    user=request.user
    favorites=Favorite.objects.get_or_create(item=product,user=user)
    
    return redirect("favorite")

