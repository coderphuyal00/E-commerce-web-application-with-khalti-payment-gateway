from django import template

register=template.Library()
@register.filter
def calculate_discount(product):
    return ((product.price-product.sale_price)/product.price)*100

@register.filter(name='format_item_count')
def item_count(count):
    if count==1:
        return f"{count} item"
    else:
        return f"{count} items"