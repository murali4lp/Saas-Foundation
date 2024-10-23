import helpers

from django.conf import settings
from django.core.management.base import BaseCommand

STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')

VENDOR_STATIC_FILES = {
    "flowbite.min.css": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css",
    "flowbite.min.js": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js",
    "flowbite.min.js.map": "https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js.map"
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