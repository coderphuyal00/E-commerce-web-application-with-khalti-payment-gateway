from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('test/',views.testPage,name='test-page'),
    path('test/view',views.get_gender,name='view-page'),
    path('forms/',views.FormList,name='form_list'),
    path('forms/add_category/',views.CategoryForm,name='add_category'),
    path('forms/add_size/',views.SizeForm,name='add_size'),
    path('forms/add_product/',views.ProductForm,name='add_product'),
    path('forms/add_productVariant/',views.ProductVariantForm,name='add_productVariant'),
    path('forms/add_productImage/',views.ProductImageForm,name='add_productImage'),
    path('products/<int:product_id>/',views.productDetail,name='product_detail'),
    path('products/delete/',views.delete_all_products,name='product_delete'),
]+ static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)