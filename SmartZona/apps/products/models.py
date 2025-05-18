from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone



class ProductCategory(models.Model):
    name = models.CharField(max_length=100, blank=True)
    zone_category = models.ForeignKey(
        'warehouse.ZoneCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )

    def __str__(self):
        return self.name


class Product(models.Model):
    UNITS = (
        ('piece', 'шт'),
        ('kg', 'кг'),
        ('liter', 'л')
        )

    name = models.CharField(max_length=255, blank=True)
    article = models.CharField(max_length=50, unique=True, blank=True)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    unit = models.CharField(max_length=10, choices=UNITS, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    storage_temperature = models.FloatField(null=True, blank=True)
    zone = models.ForeignKey(
        'warehouse.Zone',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name='items'
        )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        blank=True
        )

    def is_expired(self) -> bool:
        return (
            self.expiration_date
        ) and (
            self.expiration_date < timezone.now().date()
        )

    def assign_zone(self) -> bool:
        from SmartZona.apps.warehouse.models import Zone

        if self.zone:
            return True
        if self.category and self.category.zone_category:
            suitable_zone = (
                Zone.objects
                .filter(category=self.category.zone_category)
                .order_by('current_load')
                .first()
            )
            if suitable_zone and suitable_zone.has_space_for(self.quantity):
                self.zone = suitable_zone
                self.save()
                return True
        return False

    def save(self, *args, **kwargs):
        if not self.assign_zone():
            raise ValueError('No suitable zone found')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.article} | {self.name}"
