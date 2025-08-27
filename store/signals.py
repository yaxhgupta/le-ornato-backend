# backend/store/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MetalRate, Product

@receiver(post_save, sender=MetalRate)
def update_products_on_metalrate_change(sender, instance, created, **kwargs):
    # Example: apply to all products, or products filtered by metal type
    products = Product.objects.all()
    for p in products:
        # if you want product to pull global metal rate, set product.metal_rate = instance.rate:
        p.metal_rate = instance.rate
        p.recalculate_price()
