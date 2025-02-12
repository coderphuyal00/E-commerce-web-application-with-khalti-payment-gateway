from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Main.models import ProductVariant
from .models import Favorite,FavoriteItem
# Create your views here.
def favorites(request):
    favorite=Favorite.objects.get(user=request.user)  
    items = favorite.favoriteitem_set.all()
    context={
            "product":items,
            "favorites":favorite
        }
    return render(request,"favorites/favorite_list.html",context)
        

@login_required
def add_items_on_favorite(request,product_id):
    if request.user.is_authenticated:
        favorite_of, created=Favorite.objects.get_or_create(user=request.user)

    product=ProductVariant.objects.get(id=product_id)
    favorite_of.add_item(product)  

    return redirect("favorite")

@login_required
def remove_items_from_favorites(request,product_id,item_id):
    product=ProductVariant.objects.get(id=product_id)
    
    # item=FavoriteItem.objects.get(id=item_id)

    item=FavoriteItem.objects.get(id=item_id,item=product).delete()
    
    return redirect ("favorite")