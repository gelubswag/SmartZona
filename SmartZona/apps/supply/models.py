from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Waybill(models.Model):
    STATUSES = (
        ('pending', 'В обработке'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    )

    number = models.CharField(
        max_length=50,
        unique=True
        )
    supplier = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        )
    manager = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='waybills'
        )
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        if self.status != 'pending':
            raise ValidationError("Накладная уже обработана")
        self.status = 'accepted'
        self.save()

    def reject(self, reason: str):
        if self.status != 'pending':
            raise ValidationError("Накладная уже обработана")
        self.status = 'rejected'
        self.comment = reason
        self.save()


class WaybillItem(models.Model):
    waybill = models.ForeignKey(
        Waybill,
        on_delete=models.CASCADE,
        related_name='items'
        )
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[
            MinValueValidator(1)
            ]
        )

    def is_clean(self) -> bool:
        return self.quantity > self.product.quantity

    def __str__(self):
        return f"{self.product} x{self.quantity}"
