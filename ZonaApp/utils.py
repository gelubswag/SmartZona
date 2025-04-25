from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Требуется авторизация")
                return redirect('ZonaApp:login')
            
            try:
                staff = request.user.zonastaff  # Используем related_name
                if staff.role.name.lower() == role_name.lower():
                    return view_func(request, *args, **kwargs)
                messages.error(request, "У вас нет доступа к этой странице")
                return redirect('ZonaApp:dashboard')
            except AttributeError:
                messages.error(request, "Профиль сотрудника не найден")
                return redirect('ZonaApp:login')
        return wrapper
    return decorator