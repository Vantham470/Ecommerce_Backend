from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, ProductViewSet
from carts.views import CartViewSet
from orders.views import OrderViewSet
from payments.views import PaymentViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('cart', CartViewSet, basename='cart')
router.register('orders', OrderViewSet, basename='order')
router.register('payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token),
]