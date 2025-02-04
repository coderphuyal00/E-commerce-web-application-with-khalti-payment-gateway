from django.contrib import admin
from .models import Product,Category,ProductVariant,ProductImage,Size
# Register your models here.
# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Size)
# admin.site.register(ProductVariant)
class ProductImageInline(admin.StackedInline):
    model = ProductImage


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductVariantInline,
    ]


admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)