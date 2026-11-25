from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# ----------------------------
# HOTEL MODEL
# ----------------------------
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    image = models.ImageField(upload_to='hotel/', blank=True, null=True)

    price_per_night = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        help_text="Room price per night"
    )

    wifi = models.BooleanField(default=True)
    parking = models.BooleanField(default=True)
    air_condition = models.BooleanField(default=True)
    breakfast = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hotel Info"
        verbose_name_plural = "Hotel Info"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# ----------------------------
# CATEGORY MODEL
# ----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# ----------------------------
# GENERAL ITEM MODEL
# ----------------------------
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items"
    )

    image = models.ImageField(upload_to='items/', blank=True, null=True)

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return self.name


# ----------------------------
# SUSHI ITEM MODEL
# ----------------------------
class SushiItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='sushi_items'
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    image = models.ImageField(upload_to='sushi/', blank=True, null=True)

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sushi Item"
        verbose_name_plural = "Sushi Menu"

    def __str__(self):
        return self.name


# ----------------------------
# DELIVERY ORDER MODEL
# ----------------------------
class Order(models.Model):

    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('cod', 'Cash on Delivery'),
        ('paypay', 'PayPay'),
    ]

    DELIVERY_AREAS = [
        ('tokyo', 'Tokyo'),
        ('chiba', 'Chiba'),
        ('kanagawa', 'Kanagawa'),
    ]

    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    delivery_area = models.CharField(max_length=50, choices=DELIVERY_AREAS)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    total_amount = models.IntegerField()

    status = models.CharField(
        max_length=30,
        choices=ORDER_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"