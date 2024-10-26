import helpers

from django.conf import settings
from django.core.management.base import BaseCommand

STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')

VENDOR_STATIC_FILES = {
    "saas-theme.min.css": "https://raw.githubusercontent.com/codingforentrepreneurs/SaaS-Foundations/main/src/staticfiles/theme/saas-theme.min.css",
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    "flowbite.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map"
}

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Downloading vendor static files...")

        downloaded_urls = []
        for name, url in VENDOR_STATIC_FILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            success = helpers.download_to_local(url, out_path)

            if success:
                downloaded_urls.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f"Failed to download {url}")
                )

        if(set(downloaded_urls) == set(VENDOR_STATIC_FILES.values())):
            self.stdout.write(
                self.style.SUCCESS(f"Successfully updated all vendor static files")
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"Some files were not downloaded")
            )