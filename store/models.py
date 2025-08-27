#store/models.py
from django.db import models
from decimal import Decimal, ROUND_HALF_UP


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class MetalRate(models.Model):
    metal_name = models.CharField(max_length=50, default="Gold")
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # per gram
    effective_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metal_name} - {self.rate}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")  # <-- important

    # New fields
    metal_type = models.CharField(
        max_length=50,
        choices=[("Gold", "Gold"), ("Silver", "Silver"), ("Platinum", "Platinum")],
        default="Gold",
    )
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in grams", default=0.0)
    purity = models.CharField(max_length=50, default="22K")

    # Pricing components
    making_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="Making charges per gram")
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=3.0, help_text="GST percentage")

    def recalculate_price(self):
        try:
            metal_rate = (
                MetalRate.objects.filter(metal_name=self.metal_type)
                .order_by("-effective_date")
                .first()
            )
            if not metal_rate:
                return self.price

            metal = Decimal(metal_rate.rate)
            making = Decimal(self.making_charges)
            w = Decimal(self.weight)
            gst = Decimal(self.gst_percent)

            base = (metal + making) * w
            gst_amount = (base * gst) / Decimal(100)
            final = (base + gst_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            self.price = final
            self.save(update_fields=["price"])
            return self.price
        except Exception:
            return self.price

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through="OrderItem")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("shipped", "Shipped"), ("delivered", "Delivered")],
        default="pending",
    )

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"

    def calculate_total(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        self.total_amount = total
        self.save()
        return self.total_amount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}"

class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="banners/")  # stored in MEDIA_ROOT/banners/
    link = models.URLField(blank=True, null=True)  # optional link for clicking the banner
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title