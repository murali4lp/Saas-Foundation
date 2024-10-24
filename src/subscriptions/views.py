from django.shortcuts import render
from django.urls import reverse

from .models import SubscriptionPrice

URL_PATH_NAME = 'pricing_interval'

# Create your views here.

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