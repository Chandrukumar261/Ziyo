"""
Development settings for Ziyo E-Commerce Platform.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Allow insecure cookies for local localhost HTTP development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Console email for local dev testing
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Staticfiles in dev
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
