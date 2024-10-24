from django.contrib import admin

# Register your models here.
from .models import Subscription, UserSubscription, SubscriptionPrice

class SubscriptionPrice(admin.StackedInline):
    model = SubscriptionPrice
    extra = 0
    can_delete = False
    readonly_fields = ['stripe_id']

class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPrice]
    list_display = ['name', 'active']
    readonly_fields = ['stripe_id']

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)

