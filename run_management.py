#!/usr/bin/env python
"""
Run script for ZIYO Dedicated Management Portal.
Binds to 127.0.0.1:8001 (or custom argument).
Provides the isolated administrative portal at the root / of this website.
"""
import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    os.environ["ZIYO_PORTAL"] = "management"
    os.environ["DJANGO_ROOT_URLCONF"] = "config.urls_management"

    addrport = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1:8001"

    print("=" * 65)
    print("  ZIYO — DEDICATED MANAGEMENT & OPERATIONS PORTAL")
    print(f"  Access URL : http://{addrport}/")
    print("  Scope      : Dashboard, Products, Orders, Stock, Customers, CMS")
    print("  Storefront : Hidden from this administrative site.")
    print("=" * 65)

    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver", addrport])

if __name__ == "__main__":
    main()
