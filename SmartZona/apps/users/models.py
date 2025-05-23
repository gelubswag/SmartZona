from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class Role(models.Model):
    ROLES = [
        ('manager', 'Менеджер'),
        ('supplier', 'Поставщик'),
        ('driver', 'Водитель'),
        ('customer', 'Заказчик'),
    ]
    name = models.CharField(max_length=20, choices=ROLES, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    salary_rate = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return self.username

    def get_role(self) -> str | None:
        if self.role:
            return self.role.name
        return None

    def get_role_id(self) -> int | None:
        if self.role:
            return self.role.id
        return None

    def has_role_in(
        self,
        *roles,
        roles_list: list = None
            ) -> bool:
        if roles_list is None:
            roles_list = ()
        if self.role is None:
            return False
        return self.role.name in (roles_list + roles)
