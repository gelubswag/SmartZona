from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


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
        related_name='customer_orders'
        )
    driver = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='driver_orders'
        )
    loader = models.ForeignKey(
        'warehouse.Loader',
        on_delete=models.SET_NULL,
        null=True
        )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default='created'
        )
    created_at = models.DateTimeField(auto_now_add=True)

    def reserve_items(self):
        for item in self.items.all():
            if item.product.quantity < item.quantity:
                raise ValidationError(f"Недостаточно {item.product.name}")
            item.product.quantity -= item.quantity
            item.product.save()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.reserve_items()
        super().save(*args, **kwargs)


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
