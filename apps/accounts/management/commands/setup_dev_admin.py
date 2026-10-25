from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = "Creates the initial development administrator (ziyo / ziyo) safely for local environments."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            type=str,
            default="ziyo@example.com",
            help="Administrator email (default: ziyo@example.com)",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="ziyo",
            help="Administrator password (default: ziyo)",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR(
                    "CRITICAL: Refusing to create temporary development admin in production (DEBUG=False)."
                )
            )
            return

        email = options["email"].lower().strip()
        password = options["password"]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": "Ziyo",
                "last_name": "Admin",
                "role": User.Role.SUPERUSER,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.set_password(password)
        user.role = User.Role.SUPERUSER
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created development administrator:\n  Email: {email}\n  Password: {password}\n"
                    f"Access the management portal at /management/ or technical admin at /django-admin/"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Updated existing administrator ({email}) password to '{password}'."
                )
            )
