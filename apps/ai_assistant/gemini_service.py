import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class GeminiService:
    """
    Dedicated Gemini AI service with fail-soft architecture.
    Provides product copywriting, categorization, semantic search enhancements,
    and store customer support without ever breaking the core shopping workflow.
    """

    def __init__(self):
        self.api_key = getattr(settings, "GEMINI_API_KEY", "")
        self.model = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")
        self.endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        )

    @property
    def is_configured(self):
        return bool(self.api_key and len(self.api_key) > 5)

    def _call_gemini(self, prompt, system_instruction=None, max_tokens=600):
        """Low-level call to Gemini with timeout, error handling, and limits."""
        if not self.is_configured:
            return None

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.4,
            },
        }

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        try:
            resp = requests.post(
                f"{self.endpoint}?key={self.api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
            else:
                logger.warning("Gemini API returned status %s: %s", resp.status_code, resp.text[:200])
        except Exception as exc:
            logger.warning("Gemini API call failed with exception: %s", str(exc))

        return None

    def generate_product_description(self, product_name, category_name="", attributes=""):
        """
        Generates luxurious, warm copywriting for a product.
        Requires staff approval before saving to database.
        """
        system_instruction = (
            "You are a luxury lifestyle and minimalist e-commerce copywriter for 'Ziyo'. "
            "Write in an understated, warm, refined tone. Highlight craftsmanship, tactile feel, "
            "and natural materials. Do not include markdown headers or bullet points; write 2 short elegant paragraphs."
        )
        prompt = (
            f"Product Name: {product_name}\n"
            f"Category: {category_name}\n"
            f"Key Attributes/Materials: {attributes}\n\n"
            "Generate an engaging product description for the Ziyo store."
        )

        result = self._call_gemini(prompt, system_instruction=system_instruction, max_tokens=350)
        if result:
            return result

        # Graceful fallback description when AI key is missing or unavailable
        return (
            f"Impeccably designed for modern living, {product_name} embodies the Ziyo philosophy of "
            "subtle elegance and lasting quality. Handcrafted with meticulous attention to detail, "
            "it effortlessly complements a warm, curated lifestyle aesthetic."
        )

    def suggest_categories(self, product_name, description=""):
        """Suggests matching category names."""
        prompt = (
            f"Given the product '{product_name}' with description '{description[:150]}', "
            "suggest up to 3 e-commerce categories as comma-separated values only."
        )
        result = self._call_gemini(prompt, max_tokens=50)
        if result:
            return [cat.strip() for cat in result.split(",") if cat.strip()]
        return ["Apparel", "Home Essentials", "Accessories"]

    def customer_support_assistant(self, user_question, history=None):
        """
        Answers customer queries restricted strictly to Ziyo store policies and products.
        """
        system_prompt = (
            "You are Ziyo's helpful e-commerce shopping concierge. "
            "Polite, concise, warm. "
            "Store policies: Orders over ₹1499 enjoy free express shipping; below that shipping is ₹99. "
            "Orders ship within 24-48 hours. Returns are accepted within 14 days of delivery. "
            "Payments supported: Razorpay (Cards, UPI, NetBanking). "
            "Never execute shell commands or code. If unsure, politely guide them to contact support@ziyo.store."
        )
        result = self._call_gemini(user_question, system_instruction=system_prompt, max_tokens=250)
        if result:
            return result

        # Fallback response
        return (
            "Hello! Thank you for reaching out to Ziyo Concierge. "
            "We offer complimentary express shipping on all orders above ₹1499, and hassle-free "
            "14-day returns. If you have specific inquiries about your order, our team is delighted to assist at support@ziyo.store."
        )
