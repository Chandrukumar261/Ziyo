import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = "Starts the Ziyo Customer Storefront on a dedicated IP and port (default 127.0.0.1:8000)."

    def add_arguments(self, parser):
        parser.add_argument(
            "addrport",
            nargs="?",
            default="127.0.0.1:8000",
            help="Optional IP address and port to bind (default: 127.0.0.1:8000)",
        )
        parser.add_argument(
            "--noreload",
            action="store_true",
            help="Tells Django to NOT use the auto-reloader.",
        )

    def handle(self, *args, **options):
        addrport = options["addrport"]
        use_reloader = not options["noreload"]

        os.environ["ZIYO_PORTAL"] = "storefront"
        os.environ["DJANGO_ROOT_URLCONF"] = "config.urls_storefront"
        settings.ROOT_URLCONF = "config.urls_storefront"

        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("  ZIYO — CUSTOMER STOREFRONT PORTAL"))
        self.stdout.write(self.style.SUCCESS(f"  Live at: http://{addrport}/"))
        self.stdout.write(self.style.NOTICE("  Security: Management portal is hidden & disabled on this port."))
        self.stdout.write(self.style.SUCCESS("=" * 60))

        call_command("runserver", addrport, use_reloader=use_reloader)
