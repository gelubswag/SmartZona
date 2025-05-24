from .models import CustomUser, Role
from django.forms import ModelForm, CharField, PasswordInput


class UserRegisterForm(ModelForm):
    password = CharField(widget=PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Хэширование пароля
        if commit:
            user.save()
        return user


class UserLoginForm(ModelForm):
    password = CharField(widget=PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Хэширование пароля
        if commit:
            user.save()
        return user


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        labels = {
            'name': 'Название роли',
        }
