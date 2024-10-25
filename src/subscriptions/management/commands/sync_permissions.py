from typing import Any
from django.core.management.base import BaseCommand

from subscriptions.utils import sync_subscription_permissions


class Command(BaseCommand):

    def handle(self, *args, **options):
        sync_subscription_permissions()