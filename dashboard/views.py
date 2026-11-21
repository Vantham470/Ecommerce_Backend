from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from products.models import Product
from .serializers import AdminOrderSerializer

LOW_STOCK_LIMIT = 5
# Orders that count as real sales (not pending or cancelled)
SALE_STATUSES = ['paid', 'processing', 'shipped', 'delivered']


class LoginView(ObtainAuthToken):
    """Same as the normal login, but also returns the user's role."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })


class MeView(APIView):
    """Lets React ask 'who am I and what can I do?' using the saved token."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })


class StatsView(APIView):
    """Numbers for the dashboard home page. Staff only."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        sales = Order.objects.filter(status__in=SALE_STATUSES)
        revenue = sales.aggregate(total=Sum('total_price'))['total'] or 0

        # Sales for each of the last 7 days (days with no sales show 0)
        today = timezone.localdate()
        start = today - timedelta(days=6)
        rows = (
            sales.filter(created_at__date__gte=start)
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(total=Sum('total_price'))
        )
        by_day = {row['day']: row['total'] for row in rows}
        sales_by_day = []
        for i in range(7):
            day = start + timedelta(days=i)
            sales_by_day.append({
                'date': day.isoformat(),
                'total': float(by_day.get(day, 0)),
            })

        low_stock = list(
            Product.objects.filter(is_active=True, stock__lte=LOW_STOCK_LIMIT)
            .order_by('stock')
            .values('id', 'name', 'stock')[:10]
        )

        recent = Order.objects.select_related('user').order_by('-created_at')[:5]

        return Response({
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(status='pending').count(),
            'revenue': float(revenue),
            'customers': User.objects.filter(is_staff=False).count(),
            'low_stock': low_stock,
            'sales_by_day': sales_by_day,
            'recent_orders': AdminOrderSerializer(recent, many=True).data,
        })


class AdminOrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """All orders for staff. They can view them and change the status."""

    serializer_class = AdminOrderSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        queryset = (
            Order.objects.select_related('user')
            .prefetch_related('items')
            .order_by('-created_at')
        )
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset