"""
Base Django settings for Ziyo E-Commerce Platform.
"""

from pathlib import Path
import os
import sys
from urllib.parse import urlparse, unquote

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

# Add apps directory to sys.path
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "apps"))

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "ziyo-default-dev-secret-key-3849102384910238491023",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(",")
    if host.strip()
]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.accounts.apps.AccountsConfig",
    "apps.catalog.apps.CatalogConfig",
    "apps.inventory.apps.InventoryConfig",
    "apps.cart.apps.CartConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.payments.apps.PaymentsConfig",
    "apps.discounts.apps.DiscountsConfig",
    "apps.content.apps.ContentConfig",
    "apps.dashboard.apps.DashboardConfig",
    "apps.ai_assistant.apps.AiAssistantConfig",
    "apps.api.apps.ApiConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "apps.core.middleware.SecurityHeadersMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.AuditLoggingMiddleware",
]

# Multi-Portal Isolation & Routing Engine
# Options: 'storefront' (port 8000), 'management' (port 8001), or 'unified' (test runner)
import sys

_portal_env = os.environ.get("ZIYO_PORTAL", "").lower().strip()
if "test" in sys.argv:
    ZIYO_PORTAL = "unified"
elif _portal_env in ("management", "admin"):
    ZIYO_PORTAL = "management"
elif _portal_env == "unified":
    ZIYO_PORTAL = "unified"
else:
    ZIYO_PORTAL = "storefront"

if os.environ.get("DJANGO_ROOT_URLCONF"):
    ROOT_URLCONF = os.environ.get("DJANGO_ROOT_URLCONF")
elif ZIYO_PORTAL == "management":
    ROOT_URLCONF = "config.urls_management"
elif ZIYO_PORTAL == "storefront":
    ROOT_URLCONF = "config.urls_storefront"
else:
    ROOT_URLCONF = "config.urls"

STOREFRONT_URL = os.environ.get("STOREFRONT_URL", "http://127.0.0.1:8000/")
MANAGEMENT_URL = os.environ.get("MANAGEMENT_URL", "http://127.0.0.1:8001/")


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Ziyo custom context processors
                "apps.cart.context_processors.cart_summary",
                "apps.catalog.context_processors.catalog_context",
                "apps.content.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database Configuration
DB_ENGINE = os.environ.get("DB_ENGINE", "").strip()
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DB_ENGINE:
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": os.environ.get("DB_NAME", "ziyo_db"),
            "USER": os.environ.get("DB_USER", "ZIYO"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "Chandru26_$"),
            "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
            "PORT": os.environ.get("DB_PORT", "5432"),
            "CONN_MAX_AGE": 600,
        }
    }
elif DATABASE_URL:
    parsed_db = urlparse(DATABASE_URL)
    if parsed_db.scheme == "sqlite":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": parsed_db.path or (BASE_DIR / "db.sqlite3"),
            }
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": parsed_db.path.lstrip("/"),
                "USER": unquote(parsed_db.username) if parsed_db.username else "ZIYO",
                "PASSWORD": unquote(parsed_db.password) if parsed_db.password else "Chandru26_$",
                "HOST": parsed_db.hostname or "127.0.0.1",
                "PORT": parsed_db.port or 5432,
                "CONN_MAX_AGE": 600,
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication URLs
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "catalog:home"
LOGOUT_REDIRECT_URL = "catalog:home"

# Email Configuration
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("true", "1")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "Ziyo Support <noreply@ziyo.store>")

# Razorpay Configuration
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_test_TsE0Y4PJ65YL2o")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "qIM8BTXNF9Vhlv1qVbnpMtyv")
RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "sample_webhook_secret")
RAZORPAY_CURRENCY = os.environ.get("RAZORPAY_CURRENCY", "INR")

# Gemini AI Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

# Session & Security Settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 86400 * 14  # 2 weeks
CSRF_COOKIE_HTTPONLY = False  # Allows JS to read for HTMX/AJAX CSRF header
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# Django Messages Bootstrap/Warm Neutral Tag Mapping
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: "neutral",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

# REST Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Ziyo Custom E-Commerce & ERP API",
    "DESCRIPTION": "Server-authoritative custom APIs for Ziyo storefront, real-time order tracking, payment processing, ERP inventory synchronization, and logistics dispatch.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}

# Production Deployment Security Hardening & Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 0 if DEBUG else 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False").lower() in ("true", "1")
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False").lower() in ("true", "1")
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "False").lower() in ("true", "1")

