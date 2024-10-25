from django.urls import reverse
from helpers.billing import start_checkout_session, get_checkout_customer_plan, cancel_subscription
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseBadRequest

from django.contrib.auth import get_user_model

from subscriptions.models import Subscription, SubscriptionPrice, UserSubscription

User = get_user_model()
BASE_URL = settings.BASE_URL

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
    success_url_path = reverse('stripe-checkout-end')
    pricing_url_path = reverse('pricing')
    success_url = f"{BASE_URL}{success_url_path}"
    cancel_url = f"{BASE_URL}{pricing_url_path}"
    url = start_checkout_session(
        customer_stripe_id,
        success_url=success_url,
        cancel_url=cancel_url,
        price_stripe_id=obj.stripe_id,
        raw=False
    )
    return redirect(url)

def checkout_finalize(request):
    session_id = request.GET.get('session_id')
    checkout_data = get_checkout_customer_plan(session_id)

    customer_id = checkout_data.pop('customer_id') 
    plan_id = checkout_data.pop('plan_id')
    sub_stripe_id = checkout_data.pop('sub_stripe_id')
    subscription_data = {**checkout_data}

    try:
        sub_obj = Subscription.objects.get(subscriptionprice__stripe_id=plan_id)
    except:
        sub_obj = None

    try:
        user_obj = User.objects.get(customer__stripe_id=customer_id)
    except:
        user_obj = None

    _user_sub_exists = False
    updated_sub_options = {
        'subsciption': sub_obj,
        'stripe_id': sub_stripe_id,
        'user_cancelled': False,
        **subscription_data
    }
    try:
        _user_sub_obj = UserSubscription.objects.get(user=user_obj)
        _user_sub_exists = True
    except UserSubscription.DoesNotExist:
        _user_sub_obj = UserSubscription.objects.create(user=user_obj, **updated_sub_options)
    except:
        _user_sub_obj = None

    if None in [user_obj, sub_obj, _user_sub_obj]:
        return HttpResponseBadRequest("There was an error with your account. Please contact us.")
    
    if _user_sub_exists:
        # cancel old subscriptions
        old_stripe_id = _user_sub_obj.stripe_id
        same_stripe_id = old_stripe_id == sub_stripe_id
        if old_stripe_id is not None and not same_stripe_id:
            try:
                cancel_subscription(old_stripe_id, reason='Auto ended. New membership', feedback='other')
            except:
                pass        
        
        # assign new subscriptions
        for k, v in updated_sub_options.items():
            setattr(_user_sub_obj, k, v)
        _user_sub_obj.save()
        messages.success(request, message="Success!")
    context = {}
    return render(request, 'checkout/success.html', context)