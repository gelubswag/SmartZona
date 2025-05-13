from django.db import models


class Inventory(models.Model):
    zone = models.ForeignKey('warehouse.Zone', on_delete=models.CASCADE)
    manager = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        )
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def confirm(self):
        for item in self.items.all():
            item.product.quantity = item.actual_quantity
            item.product.save()
        self.is_confirmed = True
        self.save()


class InventoryItem(models.Model):
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='items'
        )
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    planned_quantity = models.IntegerField(editable=False)
    actual_quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.planned_quantity = self.product.quantity
        super().save(*args, **kwargs)

    @property
    def discrepancy(self):
        return self.actual_quantity - self.planned_quantity
