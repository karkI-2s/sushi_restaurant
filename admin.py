from django.contrib import admin
from .models import Hotel, Category, Item, SushiItem, Order


# ----------------------------
# HOTEL ADMIN
# ----------------------------
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price_per_night',
        'wifi',
        'parking',
        'air_condition',
        'breakfast',
        'created_at'
    )

    list_filter = (
        'wifi',
        'parking',
        'air_condition',
        'breakfast',
        'created_at'
    )

    search_fields = (
        'name',
        'description',
    )

    ordering = ('-created_at',)


# ----------------------------
# CATEGORY ADMIN
# ----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('name',)


# ----------------------------
# GENERAL ITEM ADMIN
# ----------------------------
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'available',
        'created_at'
    )

    list_filter = (
        'category',
        'available',
        'created_at'
    )

    search_fields = (
        'name',
        'description'
    )

    ordering = ('-created_at',)


# ----------------------------
# SUSHI ITEM ADMIN
# ----------------------------
@admin.register(SushiItem)
class SushiItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'available',
        'created_at'
    )

    list_filter = (
        'category',
        'available',
        'created_at'
    )

    search_fields = (
        'name',
        'description'
    )

    ordering = ('-created_at',)


# ----------------------------
# ORDER ADMIN (DELIVERY SYSTEM)
# ----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone',
        'delivery_area',
        'payment_method',
        'status',
        'total_amount',
        'created_at'
    )

    list_filter = (
        'delivery_area',
        'payment_method',
        'status',
        'created_at'
    )

    search_fields = (
        'full_name',
        'phone',
        'address'
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)