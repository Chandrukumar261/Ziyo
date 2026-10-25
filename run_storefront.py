#!/usr/bin/env python
"""
Run script for ZIYO Customer Storefront.
Binds to 127.0.0.1:8000 (or custom argument).
Completely hides and disables the management portal on this port.
"""
import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    os.environ["ZIYO_PORTAL"] = "storefront"
    os.environ["DJANGO_ROOT_URLCONF"] = "config.urls_storefront"

    addrport = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1:8000"

    print("=" * 65)
    print("  ZIYO — CUSTOMER STOREFRONT")
    print(f"  Access URL : http://{addrport}/")
    print("  Security   : Management portal is hidden & inaccessible on this port.")
    print("=" * 65)

    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver", addrport])

if __name__ == "__main__":
    main()
