from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from subscriptions.models import SubscriptionPrice

# Create your views here.

def product_price_redirect(request, price_id=None, *args, **kwargs):
    request.session['checkout_subscription_price_id'] = price_id
    return redirect('stripe-checkout-start')

@login_required
def checkout_redirect(request):
    checkout_subscription_price_id = request.session.get('checkout_subscription_price_id')
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)
    except:
        obj = None
    if not checkout_subscription_price_id or not obj:
        return redirect('pricing')
    customer_stripe_id = request.user.customer.stripe_id
    return redirect('checkout/abc')

def checkout_finalize(request):
    return
