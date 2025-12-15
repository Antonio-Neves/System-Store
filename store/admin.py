# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Customer, Sale, SaleItem, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'created_at']
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_display', 'active',
                    'created_at']
    list_filter = ['active', 'category', 'created_at']
    search_fields = ['name', 'barcode', 'description']
    list_editable = ['active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'barcode', 'image',
                       'active')
        }),
        ('Pricing', {
            'fields': ('price', 'cost')
        }),
        ('Stock', {
            'fields': ('stock', 'min_stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def stock_display(self, obj):
        if obj.is_low_stock:
            return format_html(
                '<span style="color: red; font-weight: bold;">{} ⚠️</span>',
                obj.stock
            )
        return obj.stock

    stock_display.short_description = 'Stock'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'cpf', 'total_purchases',
                    'created_at']
    search_fields = ['name', 'phone', 'email', 'cpf']
    readonly_fields = ['created_at']

    def total_purchases(self, obj):
        return obj.sales.count()

    total_purchases.short_description = 'Total Purchases'


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'subtotal']
    can_delete = False

    def subtotal(self, obj):
        return f'R$ {obj.subtotal:.2f}'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'user', 'payment_method',
                    'total_display', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['customer__name', 'user__username']
    readonly_fields = ['created_at', 'total', 'discount']
    inlines = [SaleItemInline]
    date_hierarchy = 'created_at'

    def total_display(self, obj):
        return format_html(
            '<strong style="color: green;">R$ {:.2f}</strong>',
            obj.final_total
        )

    total_display.short_description = 'Total'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'reason', 'user',
                    'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['product__name', 'reason']
    readonly_fields = ['created_at', 'user']
    date_hierarchy = 'created_at'

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


from django.contrib import admin

# Register your models here.
