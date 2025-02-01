from django.contrib import admin
from .models import Product,Category,ProductVariant,Size,ProductImage
# Register your models here.
# admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(ProductVariant)
admin.site.register(Size)
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