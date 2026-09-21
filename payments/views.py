from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from .services import process_payment
from orders.models import Order

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)

    def create(self, request):
        order = Order.objects.get(pk=request.data['order_id'], user=request.user)
        payment = process_payment(order, method=request.data.get('method', 'card'))
        return Response(self.get_serializer(payment).data, status=status.HTTP_201_CREATED)