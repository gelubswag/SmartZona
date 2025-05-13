from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    ROLES = [
        ('manager', 'Менеджер'),
        ('supplier', 'Поставщик'),
        ('storekeeper', 'Кладовщик'),
        ('driver', 'Водитель'),
        ('customer', 'Заказчик'),
    ]
    name = models.CharField(max_length=20, choices=ROLES, unique=True)


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username

    def get_role(self):
        if self.role:
            return self.role.name
        return None

    def get_role_id(self):
        if self.role:
            return self.role.id
        return None

    def has_role_in(
        self,
        *roles,
        roles_list: list = None
            ):
        return self.role.name in (roles_list + roles)
