from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from helpers.billing import get_subscription, cancel_subscription

from .models import SubscriptionPrice, UserSubscription
from subscriptions.utils import refresh_user_subscriptions

URL_PATH_NAME = 'pricing_interval'

# Create your views here.

@login_required
def user_subscription(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        completed = refresh_user_subscriptions(user_ids=[request.user.id], active_only=False)
        if completed:
            messages.success(request, message="Your plan details have been refreshed")
        else:
            messages.error(request, message="Your plan details have not beeen refreshed. Please try again.")
        return redirect(user_sub_obj.get_absolute_url())
    return render(request, 'subscriptions/user_detail_view.html', {
        'subscription': user_sub_obj
    })

@login_required
def user_subscription_cancel(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        if user_sub_obj.stripe_id and user_sub_obj.is_active_status:
            sub_data = cancel_subscription(
                user_sub_obj.stripe_id, 
                reason='User wanted to end',
                cancel_at_period_end=True,
                feedback='other',
                raw=False)
            for k,v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
            messages.success(request, message="Your plan has been cancelled")
        return redirect(user_sub_obj.get_absolute_url())
    return render(request, 'subscriptions/user_cancel_view.html', {
        'subscription': user_sub_obj
    })

def subscription_price_page(request, interval='month'):
    qs = SubscriptionPrice.objects.filter(featured=True)
    interval_month = SubscriptionPrice.IntervalChoices.MONTHLY
    interval_year = SubscriptionPrice.IntervalChoices.YEARLY
    object_list = qs.filter(interval=interval_month)

    url_path_name = URL_PATH_NAME
    monthly_url = reverse(url_path_name, kwargs={'interval': interval_month})
    yearly_url = reverse(url_path_name, kwargs={'interval': interval_year})
    active = interval_month

    if interval == interval_year:
        object_list = qs.filter(interval=interval_year)
        active = interval_year

    return render(request, 'subscriptions/pricing.html', {
        'object_list': object_list,
        'monthly_url': monthly_url,
        'yearly_url': yearly_url,
        'active': active
    })