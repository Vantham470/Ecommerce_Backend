from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product

class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def list(self, request):
        cart = self.get_object()
        return Response(self.get_serializer(cart).data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_object()
        product = Product.objects.get(pk=request.data['product_id'])
        quantity = int(request.data.get('quantity', 1))

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = item.quantity + quantity if not created else quantity
        item.save()

        return Response(self.get_serializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart = self.get_object()
        CartItem.objects.filter(cart=cart, product_id=request.data['product_id']).delete()
        return Response(self.get_serializer(cart).data, status=status.HTTP_200_OK)
