from django import template

register = template.Library()


@register.filter
def product_quantity(cart, product_id):
    item = cart.items().filter(product_id=product_id).first()
    if item is not None:
        return item.quantity
    else:
        return 0
