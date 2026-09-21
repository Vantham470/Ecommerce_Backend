from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'price', 'quantity', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'shipping_name', 'shipping_address', 'shipping_city',
                  'shipping_postal_code', 'shipping_country', 'total_price', 'items', 'created_at']
        read_only_fields = ['status', 'total_price']