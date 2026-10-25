import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.catalog.models import Category, Product, ProductReview
from apps.inventory.models import InventoryItem
from apps.discounts.models import Coupon
from apps.content.models import Banner, Page, SiteSetting

class Command(BaseCommand):
    help = "Seeds initial luxury e-commerce catalog, categories, inventory, coupons, and CMS content for Ziyo."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Ziyo database with warm minimalist essentials...")

        # 1. Categories
        apparel, _ = Category.objects.get_or_create(
            slug="apparel-linens",
            defaults={"name": "Apparel & Linens", "description": "Unstructured silhouettes crafted from raw organic linen and unbleached cotton.", "is_featured": True, "sort_order": 1}
        )
        ceramics, _ = Category.objects.get_or_create(
            slug="sculptural-ceramics",
            defaults={"name": "Sculptural Ceramics", "description": "Wheel-thrown and hand-glazed vessels with tactile matte finishes.", "is_featured": True, "sort_order": 2}
        )
        living, _ = Category.objects.get_or_create(
            slug="living-objects",
            defaults={"name": "Living & Objects", "description": "Handcrafted accents designed to harmonize residential sanctuaries.", "is_featured": True, "sort_order": 3}
        )
        lighting, _ = Category.objects.get_or_create(
            slug="ambient-lighting",
            defaults={"name": "Ambient Lighting", "description": "Warm muted illumination forged in raw brass, stone, and washi paper.", "is_featured": True, "sort_order": 4}
        )

        # 2. Products and Inventory Items
        catalog_data = [
            {
                "name": "Raw Linen Kimono Robe",
                "slug": "raw-linen-kimono-robe",
                "sku": "ZY-APP-001",
                "category": apparel,
                "price": Decimal("3450.00"),
                "compare_at_price": Decimal("4200.00"),
                "short_description": "Relaxed dropped-shoulder lounge robe woven from heavy European flax.",
                "description": "Crafted from 100% pre-washed European flax linen, this robe combines effortless lounge elegance with breathability. Features deep patch pockets, a matching tie belt, and self-finished seams for daily ritual comfort.",
                "is_featured": True,
                "is_trending": True,
                "is_new_arrival": False,
                "stock": 45,
            },
            {
                "name": "Hand-Thrown Stoneware Vessel",
                "slug": "hand-thrown-stoneware-vessel",
                "sku": "ZY-CER-002",
                "category": ceramics,
                "price": Decimal("2100.00"),
                "compare_at_price": Decimal("2500.00"),
                "short_description": "Sculptural unglazed vase with tactile sand-textured slip.",
                "description": "Each vessel is wheel-thrown individually by master ceramicists using natural stoneware clay. Left raw on the exterior to preserve natural earth texture, the interior is glazed water-tight for fresh botanicals.",
                "is_featured": True,
                "is_trending": True,
                "is_new_arrival": True,
                "stock": 25,
            },
            {
                "name": "Oatmeal Ceramic Tasting Cup",
                "slug": "oatmeal-ceramic-tasting-cup",
                "sku": "ZY-CER-003",
                "category": ceramics,
                "price": Decimal("850.00"),
                "compare_at_price": None,
                "short_description": "Ergonomic handle-free ceramic cup for pour-overs and matcha.",
                "description": "Formed to nestle naturally into palm hands, this tasting cup features an oatmeal satin glaze with delicate speckles. Dishwasher and microwave safe.",
                "is_featured": False,
                "is_trending": True,
                "is_new_arrival": False,
                "stock": 60,
            },
            {
                "name": "Sandalwood & Vetiver Botanical Candle",
                "slug": "sandalwood-vetiver-botanical-candle",
                "sku": "ZY-OBJ-004",
                "category": living,
                "price": Decimal("1250.00"),
                "compare_at_price": Decimal("1500.00"),
                "short_description": "Hand-poured coconut-soy wax in a reusable matte ceramic pot.",
                "description": "Earthy Mysore sandalwood infused with smoky Haitian vetiver and warm cedar. 55 hours of clean burning time with an unbleached cotton wick.",
                "is_featured": True,
                "is_trending": False,
                "is_new_arrival": True,
                "stock": 40,
            },
            {
                "name": "Woven Jute & Wool Textured Throw",
                "slug": "woven-jute-wool-textured-throw",
                "sku": "ZY-APP-005",
                "category": apparel,
                "price": Decimal("4800.00"),
                "compare_at_price": Decimal("5600.00"),
                "short_description": "Heavyweight tactile blanket finished with delicate raw fringe.",
                "description": "An artisanal blend of undyed sheep wool and natural jute yarn, woven on traditional shuttle looms. Delivers warm tactile comfort for winter evenings.",
                "is_featured": True,
                "is_trending": True,
                "is_new_arrival": False,
                "stock": 18,
            },
            {
                "name": "Brushed Brass Minimalist Desk Lamp",
                "slug": "brushed-brass-minimalist-desk-lamp",
                "sku": "ZY-LGT-006",
                "category": lighting,
                "price": Decimal("6200.00"),
                "compare_at_price": None,
                "short_description": "Solid brass architectural reading lamp with diffused warm LED.",
                "description": "A study in elemental geometric forms. Hand-brushed raw brass that patinas gracefully over years. Features integrated touch dimming and warm 2700K ambient light.",
                "is_featured": True,
                "is_trending": False,
                "is_new_arrival": True,
                "stock": 12,
            },
        ]

        for p_data in catalog_data:
            stock = p_data.pop("stock")
            sku = p_data["sku"]
            product, created = Product.objects.get_or_create(sku=sku, defaults=p_data)
            inv, inv_created = InventoryItem.objects.get_or_create(
                sku=sku,
                defaults={"product": product, "quantity_on_hand": stock}
            )
            if not inv_created:
                inv.quantity_on_hand = stock
                inv.save()

        # 3. Coupons
        now = timezone.now()
        one_year_later = now + datetime.timedelta(days=365)

        Coupon.objects.get_or_create(
            code="ZIYO10",
            defaults={
                "discount_type": Coupon.DiscountType.PERCENTAGE,
                "value": Decimal("10.00"),
                "min_purchase_amount": Decimal("1000.00"),
                "valid_from": now,
                "valid_to": one_year_later,
                "is_active": True,
            }
        )

        Coupon.objects.get_or_create(
            code="WELCOME200",
            defaults={
                "discount_type": Coupon.DiscountType.FIXED_AMOUNT,
                "value": Decimal("200.00"),
                "min_purchase_amount": Decimal("1200.00"),
                "valid_from": now,
                "valid_to": one_year_later,
                "is_active": True,
            }
        )

        # 4. CMS Informational Pages
        Page.objects.get_or_create(
            slug="about-us",
            defaults={
                "title": "About Ziyo",
                "content": (
                    "Founded on the principles of quiet luxury and conscious materiality, Ziyo curates living objects "
                    "that speak through texture, form, and honesty. We reject disposable trends in favor of timeless "
                    "silhouettes handcrafted by generational artisans across India and Japan.\n\n"
                    "Our products are made from renewable natural fibers, unglazed stoneware, and solid metals that "
                    "age gracefully alongside the stories of your home."
                ),
                "meta_description": "Discover the story and material philosophy behind Ziyo's curated essentials."
            }
        )

        Page.objects.get_or_create(
            slug="shipping-policy",
            defaults={
                "title": "Shipping & Delivery Policy",
                "content": (
                    "All orders are processed and carefully packaged within 24 to 48 business hours from our central fulfillment studio.\n\n"
                    "Standard express domestic delivery takes 2 to 4 business days. Orders over ₹1,499 receive complimentary "
                    "express shipping. For orders below ₹1,499, a flat delivery fee of ₹99 applies nationwide.\n\n"
                    "Real-time tracking links are transmitted via email as soon as packages are transferred to our carrier partners."
                ),
                "meta_description": "Transparent domestic express shipping policies for all Ziyo orders."
            }
        )

        Page.objects.get_or_create(
            slug="returns-refunds",
            defaults={
                "title": "Returns & Refunds Policy",
                "content": (
                    "We invite you to experience our objects with complete peace of mind. We gladly accept returns for unused, "
                    "unworn items in original packaging within 14 days of receipt.\n\n"
                    "To initiate a return, navigate to your order history and select 'Request Return', or contact concierge@ziyo.store. "
                    "Once inspected at our studio, refunds are credited back to your original payment method within 5 to 7 business days."
                ),
                "meta_description": "Our 14-day hassle-free return and refund policy."
            }
        )

        # 5. Site Settings
        SiteSetting.objects.get_or_create(key="STORE_NAME", defaults={"value": "Ziyo", "description": "Store branding name"})
        SiteSetting.objects.get_or_create(key="STORE_EMAIL", defaults={"value": "concierge@ziyo.store", "description": "Primary support email"})
        SiteSetting.objects.get_or_create(key="STORE_PHONE", defaults={"value": "+91 98765 43210", "description": "Customer care hotline"})
        SiteSetting.objects.get_or_create(key="STORE_TAGLINE", defaults={"value": "Curated Essentials, Pure Aesthetics", "description": "Brand slogan"})

        self.stdout.write(self.style.SUCCESS("Successfully seeded Ziyo catalog, inventory, and CMS content!"))
