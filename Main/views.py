from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import AddProductForm,AddCategoryForm,AddProductVariantForm,AddProductImageForm
from .models import Product,ProductImage,ProductVariant
# Create your views here.
def home(request):
    product=Product.objects.all().prefetch_related("productimage_set")
    context={
        "products":product
    }
    return render(request,'products/products.html',context)

@login_required
def FormList(request):
    return render(request,'Forms/form_list.html')

@login_required
def CategoryForm(request):
    if request.method=='POST':
        form=AddCategoryForm(request.POST)
        if form.is_valid():            
            form.save()
            return redirect('form_list')
    else:
        form=AddCategoryForm()

    return render(request,"Forms/add_category.html",{"form":form})

@login_required
def ProductForm(request):
    if request.method=='POST':
        form=AddProductForm(request.POST)
        if form.is_valid():            
            form.save()
            return redirect('form_list')
    else:
        form=AddProductForm()

    return render(request,"Forms/add_product.html",{"form":form})
@login_required
def ProductVariantForm(request):
    if request.method=='POST':
        form=AddProductVariantForm(request.POST)
        if form.is_valid():            
            form.save()
            return redirect('form_list')
    else:
        form=AddProductVariantForm()

    return render(request,"Forms/add_productVariant.html",{"form":form})
@login_required
def ProductImageForm(request):
    if request.method=='POST':
        form=AddProductImageForm(request.POST,request.FILES)
        if form.is_valid():            
            form.save()
            return redirect('form_list')
    else:
        form=AddProductImageForm()

    return render(request,"Forms/add_productImage.html",{"form":form})

def productDetail(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    product_image=ProductImage.objects.all()
    context={
        "product":product,
        "product_image":product_image
    }
    return render(request,'products/product_overview.html',context)
def testPage(request):
    if request.method=="POST":
        selected_size=request.POST.get('button_value')
    return render(request,'test.html',{'selected_size':selected_size})

def delete_all_products(request):
    product=Product.objects.all()
    product.delete()
    
    return HttpResponse("Products deleted successfully.")