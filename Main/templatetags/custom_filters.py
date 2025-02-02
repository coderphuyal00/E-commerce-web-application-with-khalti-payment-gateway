from django import template

register=template.Library()
@register.filter
def calculate_discount(product):
    return ((product.price-product.sale_price)/product.price)*100