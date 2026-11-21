from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import CategoryViewSet, ProductViewSet
from carts.views import CartViewSet
from orders.views import OrderViewSet
from payments.views import PaymentViewSet
from dashboard.views import LoginView, MeView, StatsView, AdminOrderViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('cart', CartViewSet, basename='cart')
router.register('orders', OrderViewSet, basename='order')
router.register('payments', PaymentViewSet, basename='payment')
router.register('admin/orders', AdminOrderViewSet, basename='admin-order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view()),
    path('api/me/', MeView.as_view()),
    path('api/admin/stats/', StatsView.as_view()),
]