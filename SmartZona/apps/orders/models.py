from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Order(models.Model):
    STATUSES = (
        ('created', 'Создан'),
        ('processing', 'Собирается'),
        ('delivering', 'В пути'),
        ('delivered', 'Доставлен'),
    )

    customer = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='customer_orders',
        blank=True
        )
    driver = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='driver_orders',
        blank=True,
        default=None
        )
    loader = models.ForeignKey(
        'warehouse.Loader',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
        )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default='created'
        )
    created_at = models.DateTimeField(auto_now_add=True)

    def has_enough_items(self) -> bool:
        for item in OrderItem.objects.filter(order=self).all():
            if item.product.quantity < item.quantity:
                return False
        return True

    def reserve_items(self) -> bool:
        if not self.has_enough_items():
            return False

        for item in OrderItem.objects.filter(order=self).all():
            item.product.quantity -= item.quantity
            item.product.save()

    def total_items(self) -> int:
        return self.items.count()

    def clean(self):
        if self.status == 'processing' and self.total_items() == 0:
            raise ValidationError("Нельзя отправить пустой заказ на сборку")


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
        )
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.product} x{self.quantity}"

    def clean(self):
        if self.quantity > self.product.quantity:
            raise ValidationError(f"Недостаточно товара {self.product.name}")
