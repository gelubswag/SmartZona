from django.db import models
from django.core.validators import MinValueValidator
from SmartZona.apps.products.models import Product


class ZoneCategory(models.Model):
    STORAGE_TYPES = (('refrigerator', 'Холодильник'), ('rack', 'Стеллаж'))
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=STORAGE_TYPES)
    temperature = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Zone(models.Model):
    code = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(ZoneCategory, on_delete=models.PROTECT)
    capacity = models.FloatField(validators=[MinValueValidator(0.1)])

    @property
    def current_load(self) -> int:
        return sum(
            product.quantity
            for product in Product.objects.filter(zone=self).all()
            )

    def has_space_for(self, products: list[Product]) -> bool:
        return (
            self.current_load + sum(
                product.quantity for product in products
            )
                ) <= self.capacity

    def __str__(self):
        return f"Зона {self.code} | {self.category}"


class Loader(models.Model):
    TYPES = (('electric', 'Электрический'), ('manual', 'Ручной'))
    type = models.CharField(max_length=20, choices=TYPES)
    load_capacity = models.FloatField(validators=[MinValueValidator(0.1)])
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_type_display()} | {self.load_capacity}кг"
