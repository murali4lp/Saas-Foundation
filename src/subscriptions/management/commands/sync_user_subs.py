from typing import Any
from django.core.management.base import BaseCommand
from subscriptions.utils import clear_dangling_subs, refresh_user_subscriptions


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--day-start", default=0, type=int)
        parser.add_argument("--day-end", default=0, type=int)
        parser.add_argument("--days-left", default=0, type=int)
        parser.add_argument("--days-ago", default=0, type=int)
        parser.add_argument("--clear-dangling", action="store_true", default=False)

    def handle(self, *args, **options):
        days_left = options.get("days_left")
        days_ago = options.get("days_ago")
        day_start = options.get("day_start")
        day_end = options.get("day_end")
        clear_dangling = options.get('clear_dangling')
        if clear_dangling:
            print('Clearing dangling active stripe subscriptions not in use')
            clear_dangling_subs()
        else:
            print('Sync active subs')
            done = refresh_user_subscriptions(
                        active_only=True, 
                        days_left=days_left,
                        days_ago=days_ago,
                        day_start=day_start,
                        day_end=day_end,
                        verbose=True
                    )
            if done: 
                print('Done')