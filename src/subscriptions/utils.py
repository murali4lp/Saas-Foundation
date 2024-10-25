from helpers.billing import get_customer_active_subscriptions, cancel_subscription, get_subscription
from customers.models import Customer
from subscriptions.models import UserSubscription, Subscription

def refresh_user_subscriptions(
        user_ids=None, 
        active_only=True, 
        days_left=-1,
        days_ago=-1,
        day_start=-1,
        day_end=-1,
        verbose=False):
    qs = UserSubscription.objects.all()
    if active_only:
        qs = qs.by_active_trialing()
    if user_ids is not None:
        qs = qs.by_user_ids(user_ids=user_ids)
    if days_ago > -1:
        qs = qs.by_days_ago(days_ago=days_ago)
    if days_left > -1:
        qs = qs.by_days_left(days_left=days_left)
    if day_start > -1 and day_end > -1:
        qs = qs.by_range(days_start=day_start, days_end=day_end, verbose=verbose)
    
    complete_count = 0
    qs_count = qs.count()
    for obj in qs:
        if verbose:
            print("Updating user", obj.user, obj.subscription, obj.current_period_end)
        if obj.stripe_id:
            sub_data = get_subscription(obj.stripe_id, raw=False)
            for k,v in sub_data.items():
                setattr(obj, k, v)
            obj.save()
            complete_count+=1
    return complete_count == qs_count

def clear_dangling_subs():
    qs = Customer.objects.filter(stripe_id__isnull=False)
    for customer_obj in qs:
        user = customer_obj.user
        customer_stripe_id = customer_obj.stripe_id
        print(f"Sync {user} with stripe id - {customer_stripe_id} subs and remove old ones")
        subs = get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            existing_user_subs_qs = UserSubscription.objects.filter(
                stripe_id__isexact=f"{sub.id}".strip()
            )
            if existing_user_subs_qs.exists():
                continue
            cancel_subscription(
                stripe_id=sub.id,
                cancel_at_period_end=False,
                reason='Dangling active susbcriptions'
            )


def sync_subscription_permissions():
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            sub_perms = obj.permissions.all()
            for group in obj.groups.all():
                group.permissions.set(sub_perms)