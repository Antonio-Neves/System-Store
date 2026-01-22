from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=5,
                                    help_text="Minimum stock level alert")
    barcode = models.CharField(max_length=50, blank=True, unique=True,
                               null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock

    @property
    def profit_margin(self):
        if self.cost > 0:
            return ((self.price - self.cost) / self.cost) * 100
        return 0


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    cpf = models.CharField(max_length=14, blank=True, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# class Sale(models.Model):
#     PAYMENT_METHODS = [
#         ('cash', 'Dinheiro'),
#         ('debit', 'Cartão de Débito'),
#         ('credit', 'Cartão de Crédito'),
#         ('pix', 'PIX'),
#     ]
#
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,
#                                  null=True, blank=True, related_name='sales')
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
#                              related_name='sales')
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS,
#                                       default='cash')
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     notes = models.TextField(blank=True)
#     created_at = models.DateTimeField(default=timezone.now)
#
#     class Meta:
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"Sale #{self.id} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
#
#     @property
#     def final_total(self):
#         return self.total - self.discount


class Sale(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Dinheiro'),
        ('debit', 'Cartão de Débito'),
        ('credit', 'Cartão de Crédito'),
        ('pix', 'PIX'),
        ('transferencia', 'Transferência Bancária'),
    ]

    STATUS_CHOICES = [
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='sales')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             related_name='sales')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS,
                                      default='cash')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='completed')  # NEW
    cancelled_at = models.DateTimeField(null=True, blank=True)  # NEW
    cancellation_reason = models.TextField(blank=True)  # NEW
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='cancelled_sales')  # NEW
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Sale #{self.id} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

    @property
    def final_total(self):
        return self.total - self.discount

    @property
    def is_cancelled(self):  # NEW
        return self.status == 'cancelled'


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE,
                             related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='sale_items')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.quantity * self.price


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Saída'),
        ('adjustment', 'Ajuste'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"


from django.db import models

# Create your models here.
