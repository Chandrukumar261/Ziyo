import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = "Starts the Ziyo Dedicated Management Portal on a separate IP and port (default 127.0.0.1:8001)."

    def add_arguments(self, parser):
        parser.add_argument(
            "addrport",
            nargs="?",
            default="127.0.0.1:8001",
            help="Optional IP address and port to bind (default: 127.0.0.1:8001)",
        )
        parser.add_argument(
            "--noreload",
            action="store_true",
            help="Tells Django to NOT use the auto-reloader.",
        )

    def handle(self, *args, **options):
        addrport = options["addrport"]
        use_reloader = not options["noreload"]

        os.environ["ZIYO_PORTAL"] = "management"
        os.environ["DJANGO_ROOT_URLCONF"] = "config.urls_management"
        settings.ROOT_URLCONF = "config.urls_management"

        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("  ZIYO — DEDICATED MANAGEMENT & OPERATIONS PORTAL"))
        self.stdout.write(self.style.SUCCESS(f"  Live at: http://{addrport}/"))
        self.stdout.write(self.style.NOTICE("  Features: Catalog, Stock, Orders, CRM, Settings, Audit"))
        self.stdout.write(self.style.NOTICE("  Storefront browsing is isolated from this administrative port."))
        self.stdout.write(self.style.SUCCESS("=" * 60))

        call_command("runserver", addrport, use_reloader=use_reloader)
