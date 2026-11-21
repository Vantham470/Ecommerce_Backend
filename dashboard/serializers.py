from rest_framework import serializers

from orders.models import Order
from orders.serializers import OrderItemSerializer

class AdminOrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.username', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'status',
            'shipping_name', 'shipping_address', 'shipping_city',
            'shipping_postal_code', 'shipping_country',
            'total_price', 'items', 'created_at',
        ]

        # Staff may only change the status, nothing else 
        
        read_only_fields = [
            'id', 'customer', 'shipping_name', 'shipping_address', 'shipping_city',
            'shipping_postal_code', 'shipping_country', 'total_price', 'items', 'created_at',
        ]