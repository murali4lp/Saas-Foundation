"""
URL configuration for saas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from .views import (
    home_page, 
    about_page, 
    pw_protected_page,
    staff_only_page,
    user_only_page
)
from auth.views import login_view, register_view
from landing.views import landing_dashboard_page
from subscriptions.views import subscription_price_page, user_subscription, user_subscription_cancel
from checkouts.views import checkout_redirect, checkout_finalize, product_price_redirect

urlpatterns = [
    path('', landing_dashboard_page, name='home'),
    path('checkout/sub-price/<int:price_id>/', product_price_redirect, name='sub-price-checkout'),
    path('checkout/start/', checkout_redirect, name='stripe-checkout-start'),
    path('checkout/success/', checkout_finalize, name='stripe-checkout-end'),
    path('pricing/', subscription_price_page, name='pricing'),
    path('pricing/<str:interval>', subscription_price_page, name='pricing_interval'),
    path('about/', about_page),
    path('accounts/billing/', user_subscription, name='user_subscription'),
    path('accounts/billing/cancel', user_subscription_cancel, name='user_subscription_cancel'),
    path('accounts/', include('allauth.urls')),
    path('protected/', pw_protected_page),
    path('protected/user-only/', user_only_page),    
    path('protected/staff-only/', staff_only_page),
    path('profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
]
