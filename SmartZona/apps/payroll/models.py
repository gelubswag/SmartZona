from django.db import models
from django.core.validators import MinValueValidator


class SalaryReport(models.Model):
    date = models.DateField()
    manager = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    total_amount = models.FloatField(editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    @property
    def get_date(self):
        return self.date.strftime('%d.%m.%Y')

    def __str__(self):
        return f"Отчёт за {self.date.strftime('%d.%m.%Y')}"


class Salary(models.Model):
    from SmartZona.apps.users.models import CustomUser

    report = models.ForeignKey(SalaryReport, on_delete=models.CASCADE)
    worker = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    shifts_worked = models.IntegerField(
        default=0, validators=[MinValueValidator(0)]
        )

    @property
    def salary_amount(self):
        return self.worker.salary_rate * self.shifts_worked

    def __str__(self):
        return f"{self.worker} - {self.salary_amount}"
