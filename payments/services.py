from django.db import transaction
from .models import Payment

@transaction.atomic
def process_payment(order, method='card'):
    """
    Simulates sending a payment to a gateway and getting a result back.
    In a real system, this is where you'd call Stripe/PayPal's API instead.
    """
    payment = Payment.objects.create(
        order=order,
        method=method,
        amount=order.total_price,
        status='pending',
    )

    # Simulated gateway response — always succeeds for now
    payment_success = True

    if payment_success:
        payment.status = 'completed'
        payment.save()
        order.status = 'paid'
        order.save()
    else:
        payment.status = 'failed'
        payment.save()

    return payment