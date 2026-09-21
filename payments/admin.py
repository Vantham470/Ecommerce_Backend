from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'method', 'status', 'amount', 'created_at')
    list_filter = ('status', 'method')
    readonly_fields = ('transaction_id',)
