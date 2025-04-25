from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class StaffRole(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name


class LoaderCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name


class Loader(models.Model):
    category = models.ForeignKey(LoaderCategory, on_delete=models.CASCADE)
    load_capacity = models.FloatField(validators=[MinValueValidator(0.1)])
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.category} {self.load_capacity}кг'


class ZonaStaff(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=True, null=False,
        related_name='zonastaff'
        )
    role = models.ForeignKey(StaffRole, on_delete=models.CASCADE)
    salary = models.FloatField(
        default=0.01,
        validators=[MinValueValidator(0.1)]
        )

    def __str__(self):
        return str(self.role) + " " + str(self.user.username)


class ZoneCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    capacity = models.FloatField(
        default=0.01,
        validators=[MinValueValidator(0.1)]
        )
    current_load = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0
        )
    temperature_mode = models.FloatField(default=0)
    zone_type = models.ForeignKey(
        ZoneCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def has_space(self, new_item: 'Item'):
        return self.capacity > self.current_load + new_item.quantity

    @property
    def get_current_load(self):
        zone_items = Item.objects.filter(zone=self)
        return sum([item.quantity for item in zone_items])


class ItemCategory(models.Model):
    name = models.CharField(max_length=100)
    zone_type = models.ForeignKey(
        ZoneCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0.1)],
        default=1
        )
    article = models.CharField(max_length=100, unique=True, null=False)
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )
    expiration_date = models.DateField(
        null=True,
        blank=True,
        )
    storage_temperature = models.FloatField(
        null=True,
        blank=True,
    )
    zone_id = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )

    def check_expiration_date(self) -> bool:
        if self.expiration_date:
            if self.expiration_date < datetime.now().date():
                return True
        return False

    def save(self, *args, **kwargs):
        if not self.zone_id and self.category and self.category.zone_type:
            suitable_zone = Zone.objects.filter(
                zone_type=self.category.zone_type,
                status=True
            ).order_by('current_load').first()
            if suitable_zone:
                if suitable_zone.has_space(self):
                    
                    self.zone_id = suitable_zone
                    suitable_zone.current_load += self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"""{
            [f"Годен до {self.expiration_date}", "Срок годности истек"][
             self.check_expiration_date()
            ]
            } {self.name}x{self.quantity}"""


class Waybill(models.Model):
    status = models.CharField(
        max_length=100,
        choices=[
            ('in_progress', 'В обработке'),
            ('accepted', 'Подтверждено'),
            ('declined', 'Отклонено')
        ]
        )
    staff_id = models.ForeignKey(
        ZonaStaff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    comment = models.TextField(blank=True, null=True)

    def accept(self):
        self.status = 'accepted'
        self.save()

    def deceline(self, reason):
        self.status = 'declined'
        self.comment = reason
        self.save()


class WaybillItem(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
        )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0.1)],
        default=1
        )
    waybill = models.ForeignKey(
        Waybill,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return f"{self.item.name}x{self.quantity}"


class DecelinedWaybill(models.Model):
    waybill = models.ForeignKey(
        Waybill,
        on_delete=models.CASCADE
        )
    reason = models.CharField(
        max_length=100
        )

    def __str__(self):
        return f"{self.waybill} - {self.reason}"


class Order(models.Model):
    status = models.CharField(
        max_length=100,
        choices=[
            ('created', 'Создан'),
            ('in_progress', 'Cобирается'),
            ('on_the_way', 'В пути'),
            ('delivered', 'Доставлен'),
        ]
        )
    created_at = models.DateTimeField(
        auto_now_add=True
        )
    updated_at = models.DateTimeField(
        auto_now=True
        )

    def __str__(self):
        return f"{self.id} - {self.status}"


class OrderItem(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
        )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0.1)],
        default=1
        )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
        )

    def save(self, *args, **kwargs):
        if self.quantity > self.item.quantity:
            return False
        self.item.quantity -= self.quantity
        self.item.save()
        super().save(*args, **kwargs)
        return True

    def __str__(self):
        return f"{self.item} - {self.quantity} - {self.order}"


class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_license = models.CharField(max_length=100)
    working_at = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    loader = models.ForeignKey(
        Loader,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user} - {self.driver_license}"

    def take_order(self, order: Order) -> bool:
        self.working_at = order
        order.status = 'on_the_way'
        order.save()
        self.save()
        return self.working_at is not None

    def confirm_deliver(self) -> bool:
        if self.working_at is not None:
            self.working_at.status = 'delivered'
            self.working_at.save()
            self.working_at = None
            self.save()
        return self.working_at is None


class InventoryReport(models.Model):
    date = models.DateField(
        auto_now_add=True
        )
    zone_id = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )

    def create_PDF_report(self):
        pass  # TODO

    def commit_changes(self):
        items = InventoryReportItem.objects.filter(
            inventory_report=self
            ).all()
        for item in items:
            item.item.quantity = item.quantity
            item.item.save()
        self.date = datetime.now()

    def __str__(self):
        return f'{self.date} - {self.zone_id}'


class InventoryReportItem(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
        )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0.1)],
        default=1
        )
    inventory_report = models.ForeignKey(
        InventoryReport,
        on_delete=models.CASCADE
        )

    def validate_date(self):
        return self.item.expiration_date > self.inventory_report.date
    
    @property
    def planned_quantity(self):
        return self.item.quantity

    @property
    def difference(self):
        return self.planned_quantity - self.quantity

    @property
    def status(self):
        if self.difference == 0:
            return 'Соответствует'
        elif self.difference > 0:
            return 'Избыток'
        else:
            return 'Недостаток'

    def __str__(self):
        return f'{self.inventory_report.id} - {self.item} - {self.quantity}'


class SalaryStatement(models.Model):
    date = models.DateField(
        auto_now_add=True
        )
    statement = models.JSONField(null=False)
    is_aproved = models.BooleanField(default=False)

    def calculate_salary(self):
        staff_objs = ZonaStaff.objects.all()
        for staff in staff_objs:
            self.statement[staff.user.username] = staff.salary

        self.save()
        return self.statement

    def export_to_pdf(self):
        return self.statement  # TODO: Implement PDF export

    def __str__(self):
        return f'{self.date} - {self.statement}'
