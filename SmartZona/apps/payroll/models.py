from django.db import models

from SmartZona.apps.users.models import CustomUser


class SalaryReport(models.Model):
    month = models.DateField()
    manager = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        )
    total_amount = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now=True)

    def calculate_salary(self):
        total = 0
        for staff in CustomUser.objects.filter(
            role__in=['manager', 'storekeeper', 'driver']
                ):
            total += staff.salary
        self.total_amount = total
        self.save()
        return self.total_amount

    def __str__(self):
        return f"Отчёт за {self.month.strftime('%B %Y')}"
