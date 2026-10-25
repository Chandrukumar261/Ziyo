# Ziyo — Complete E-Commerce Platform

Ziyo is an intentional, production-grade e-commerce web platform inspired by warm minimalist aesthetics ([Dribbble inspiration](https://dribbble.com/shots/27558664-Mobile-Ecommerce-App)), engineered with **Django 5.1 LTS**, **PostgreSQL**, **Razorpay payments**, **Gemini AI assistance**, **HTMX/Vanilla modern frontend**, and a separate **`/management/` business operations portal**.

---

## 1. System Architecture & Boundaries

```
[ Customer Browser / Mobile Viewport ]
       │                ▲
       ▼                │
┌────────────────────────────────────────────────────────┐
│             Nginx Reverse Proxy / SSL (443)            │
│   - Security Headers (HSTS, CSP, X-Frame-Options)      │
│   - Static Asset Caching & Media Passthrough           │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│            Gunicorn Application Server                 │
│                                                        │
│  ┌─────────────────────────┐  ┌─────────────────────┐  │
│  │   Customer Storefront   │  │ Management Portal   │  │
│  │   (/, /cart/, /orders/) │  │ (/management/)      │  │
│  └───────────┬─────────────┘  └──────────┬──────────┘  │
│              │                           │             │
│              ▼                           ▼             │
│  ┌──────────────────────────────────────────────────┐  │
│  │                 Core Services Layer              │  │
│  │  - Cart & Price Authority (Server-side Decimal)  │  │
│  │  - Inventory Locking & Reservation Engine        │  │
│  │  - Razorpay HMAC Payment Verification            │  │
│  │  - Webhook Idempotency Ledger                    │  │
│  │  - Gemini AI Fail-Soft Copywriting & Concierge   │  │
│  │  - Immutable Security & Compliance Audit Log     │  │
│  └──────────────────────────────────────────────────┘  │
└───────────────────────┬────────────────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
┌─────────────────────────┐   ┌──────────────────────────┐
│   PostgreSQL Database   │   │  Redis Cache & Sessions  │
│   (Transactions, ACID)  │   │  (Celery / Session)      │
└─────────────────────────┘   └──────────────────────────┘
```

---

## 2. Complete Project Directory Structure

```
ziyo/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       └── production.py
├── apps/
│   ├── core/                  # Base models, AuditLog, custom error handlers, middleware
│   ├── accounts/              # Custom User, UserProfile, CustomerAddress, auth views
│   ├── catalog/               # Category, Product, ProductImage, ProductVariant, Reviews
│   ├── inventory/             # InventoryItem, StockMovement, StockReservation (row locks)
│   ├── cart/                  # Cart, CartItem, Wishlist, authoritative CartService
│   ├── orders/                # Order, OrderItem snapshot, status history, shipments
│   ├── payments/              # Payment, RazorpayService, HMAC signature check, webhooks
│   ├── discounts/             # Coupon, validation rules, redemption tracking
│   ├── content/               # Banners, Pages, SiteSetting, Newsletter
│   ├── dashboard/             # Separate staff management interface at /management/
│   └── ai_assistant/          # Gemini AI integration, fail-soft fallback copywriting
├── templates/
│   ├── base.html              # Master storefront layout
│   ├── storefront/            # Home, product list, product details, category, contact
│   ├── cart/                  # Cart detail, wishlist
│   ├── checkout/              # Checkout form, Razorpay payment gateway, failure page
│   ├── orders/                # Order history, order detail, receipt, return request
│   ├── accounts/              # Sign in, register, customer profile, address CRUD
│   ├── admin_dashboard/       # Complete /management/ portal layouts and CRUD views
│   └── errors/                # Custom 400, 403, 404, 500 pages
├── static/
│   ├── css/
│   │   ├── style.css          # Master warm neutral storefront design system
│   │   └── admin.css          # Executive management dashboard stylesheet
│   ├── js/
│   │   ├── main.js            # Steppers, gallery switcher, AI support concierge
│   │   └── admin.js           # Admin dashboard & AI copywriting trigger
│   └── images/                # Vector placeholders & logo assets
├── tests/
│   ├── test_authentication.py
│   ├── test_catalog_crud.py
│   ├── test_cart_checkout.py
│   ├── test_payments_webhook.py
│   ├── test_security_access.py
│   └── test_customer_journey_e2e.py
├── deployment/
│   └── nginx.conf             # Production Nginx reverse proxy with SSL & headers
└── scripts/
    ├── backup_db.sh           # Automated compressed PostgreSQL backup
    └── restore_db.sh          # PostgreSQL restoration script
```

---

## 3. Brand & Design System

The visual design is inspired by modern luxury e-commerce with a warm, organic color palette:
- **Backgrounds:** Cream & warm off-white (`#FAF8F5`, `#F3EFEA`, `#FFFFFF`)
- **Typography:** Charcoal primary headings (`#1C1917`), warm muted body text (`#57534E`, `#8C867F`)
- **Accents:** Muted earth taupe & bronze (`#8C7051`, hover `#735A3E`, soft `#F4EFEB`)
- **Badges:** Terracotta for discounts (`#C86D51`), sage green for fresh releases (`#5F7A69`)
- **Cards & Shadows:** 14px border radius, 1px subtle neutral border (`rgba(28,25,23,0.08)`), delicate hover elevation (`translateY(-4px)`).
- **Mobile Viewport:** Bottom navigation dock with quick access to Home, Shop, Wishlist, Cart, and Account.

---

## 4. Local Development Setup

### Prerequisites
- Python 3.12+ or 3.13+
- Git

### Quickstart Commands

```bash
# 1. Navigate to the project directory
cd ziyo

# 2. Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# 3. Install pinned dependencies
pip install -r requirements.txt

# 4. Copy environment configuration
cp .env.example .env

# 5. Apply database migrations (SQLite by default in dev)
python manage.py migrate

# 6. Seed initial curated catalog, inventory, and coupons
python manage.py seed_ziyo_data

# 7. Create initial development administrator
python manage.py setup_dev_admin

# 8. Start development server
python manage.py runserver
```

Open your browser:
- **Storefront:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Management Portal:** [http://127.0.0.1:8000/management/](http://127.0.0.1:8000/management/)
- **Technical Admin:** [http://127.0.0.1:8000/django-admin/](http://127.0.0.1:8000/django-admin/)

---

## 5. Initial Administrator Credentials

For local development only:
- **Email:** `ziyo@example.com`
- **Password:** `ziyo`

> **Security Warning:** The `setup_dev_admin` command strictly refuses to execute when `DEBUG=False`. In production, use standard `python manage.py createsuperuser` with a strong, unique secret.

---

## 6. PostgreSQL Database Configuration

### Production Setup

1. Install PostgreSQL 15+ or 16:
```bash
sudo apt update && sudo apt install postgresql postgresql-contrib
```

2. Create database and restricted user:
```sql
sudo -u postgres psql
CREATE DATABASE ziyo_db;
CREATE USER ziyo_app WITH ENCRYPTED PASSWORD 'replace_with_strong_password';
GRANT ALL PRIVILEGES ON DATABASE ziyo_db TO ziyo_app;
\c ziyo_db
GRANT ALL ON SCHEMA public TO ziyo_app;
\q
```

3. Update `.env`:
```ini
DATABASE_URL=postgresql://ziyo_app:replace_with_strong_password@localhost:5432/ziyo_db
```

4. Apply migrations:
```bash
python manage.py migrate
```

---

## 7. Payment Gateway (Razorpay) & Idempotency

1. Set your test or production credentials in `.env`:
```ini
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...
RAZORPAY_WEBHOOK_SECRET=...
```

2. **Server-Side Verification:**
   - Client checkout submits `razorpay_order_id`, `razorpay_payment_id`, and `razorpay_signature`.
   - The server validates HMAC-SHA256 signature against `RAZORPAY_KEY_SECRET` in constant time (`hmac.compare_digest`).
   - Tampered signatures are rejected immediately.

3. **Webhook Idempotency:**
   - Webhook deliveries at `/payments/webhook/razorpay/` verify `X-Razorpay-Signature`.
   - Incoming events are recorded in `PaymentWebhookEvent(event_id)`.
   - Replay deliveries matching existing processed event IDs are acknowledged with HTTP 200 without duplicate inventory deductions or double captures.

4. **Sandbox Simulation Mode:**
   - For offline or local development, the payment page includes an interactive **"Simulate Success"** and **"Simulate Failed Sig"** button to thoroughly test both success and failure flows without live credentials.

---

## 8. Gemini AI Integration (Fail-Soft)

- Set `GEMINI_API_KEY` in `.env`.
- Service features:
  - **AI Copywriting Assistance:** Available on product edit/create forms in `/management/products/`. Clicking **"Generate with Gemini AI"** suggests luxury descriptions that staff can review and edit before saving.
  - **Customer Support Concierge:** Floating chat widget on the storefront answering store inquiries (shipping, returns, care) with strict system prompts.
  - **Fail-Soft Guarantee:** If the API key is not configured, rate-limited, or network fails, the service transparently serves pre-crafted rule-based responses without breaking the shopping cart or checkout.

---

## 9. Automated Testing

Run the automated test suites covering authentication, CRUD, cart price integrity, webhooks, security isolation, and the complete end-to-end journey:

```bash
# Run all test suites
python manage.py test tests -v 2
```

All 15 tests pass out of the box:
```
test_customer_registration_success (tests.test_authentication) ... ok
test_registration_password_mismatch_rejected (tests.test_authentication) ... ok
test_customer_login_and_logout (tests.test_authentication) ... ok
test_product_creation_and_inventory_link (tests.test_catalog_crud) ... ok
test_product_soft_deletion_archiving (tests.test_catalog_crud) ... ok
test_add_to_cart_and_totals_calculation (tests.test_cart_checkout) ... ok
test_checkout_creates_order_and_reserves_inventory (tests.test_cart_checkout) ... ok
test_payment_callback_valid_signature_settles_order_and_inventory (tests.test_payments_webhook) ... ok
test_payment_callback_invalid_tampered_signature_rejected (tests.test_payments_webhook) ... ok
test_duplicate_webhook_protection_is_idempotent (tests.test_payments_webhook) ... ok
test_anonymous_guest_management_access_redirects_to_staff_login (tests.test_security_access) ... ok
test_ordinary_customer_management_access_raises_403_forbidden (tests.test_security_access) ... ok
test_authorized_staff_can_access_management (tests.test_security_access) ... ok
test_customer_cannot_view_another_customers_order (tests.test_security_access) ... ok
test_full_customer_and_admin_lifecycle (tests.test_customer_journey_e2e) ... ok
```

---

## 10. Docker Deployment

Launch PostgreSQL, Redis, and Django in a reproducible production container stack:

```bash
# Build and run containers
docker-compose up --build -d

# Check status
docker-compose ps

# Apply migrations inside web container
docker-compose exec web python manage.py migrate

# Seed data
docker-compose exec web python manage.py seed_ziyo_data
```

---

## 11. Database Backup & Recovery

```bash
# Run backup
bash scripts/backup_db.sh

# Restore from backup
bash scripts/restore_db.sh /var/backups/ziyo/ziyo_db_YYYYMMDD_HHMMSS.sql.gz
```

---

## 12. Security Audit Checklist

- [x] Passwords hashed with Django's PBKDF2/SHA256 (never plaintext).
- [x] Server-side price authority: all line prices and order totals recalculated on the server.
- [x] Atomic transactions (`transaction.atomic`) and row-locking (`select_for_update`) prevent inventory race conditions.
- [x] CSRF protection enabled on all mutating forms.
- [x] Strictly protected `/management/` portal: ordinary customers receive HTTP 403 Forbidden.
- [x] Cryptographic HMAC-SHA256 signature verification on Razorpay payment callbacks.
- [x] Webhook duplicate delivery deduplication.
- [x] Soft-delete archiving prevents destructive deletion of ordered catalog records.
- [x] AuditLog records all mutating actions, logins, payments, and refunds.
