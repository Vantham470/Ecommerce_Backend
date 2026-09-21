from django.db import transaction
from .models import Order, OrderItem

@transaction.atomic
def create_order_from_cart(cart, shipping_info):
    if not cart.items.exists():
        raise ValueError("Cannot create an order from an empty cart")

    order = Order.objects.create(
        user=cart.user,
        total_price=cart.total_price,
        **shipping_info  # shipping_name, shipping_address, etc.
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
        )

    cart.items.all().delete()  # clear the cart after checkout
    return order