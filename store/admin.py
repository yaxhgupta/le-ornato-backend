#store/admin.py
from django.contrib import admin
from .models import Product, MetalRate, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "metal_type", "weight", "price", "stock")  # Added category
    search_fields = ("name",)
    list_filter = ("metal_type", "purity", "category")  # Added category to filters

@admin.register(MetalRate)
class MetalRateAdmin(admin.ModelAdmin):
    list_display = ("metal_name", "rate", "effective_date")
    ordering = ("-effective_date",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "rating", "created_at")
    search_fields = ("name", "comment")
