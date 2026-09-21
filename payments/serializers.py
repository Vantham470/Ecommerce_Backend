from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'transaction_id', 'method', 'status', 'amount', 'created_at']
        read_only_fields = ['transaction_id', 'status']