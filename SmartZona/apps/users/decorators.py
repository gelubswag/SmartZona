from typing import List, Any, Callable
from functools import wraps
from django.http.response import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect, render


def allowed_roles(
    roles: List[str],
    view_not_authorized: HttpResponse = HttpResponseForbidden,
    view_forbidden: HttpResponse = HttpResponseForbidden,
) -> Callable:
    def decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def wrapper(request, *args: Any, **kwargs: Any) -> Any:
            if hasattr(request, "user"):
                user = request.user
            else:
                user = request.user

            if not user.is_authenticated:
                return view_not_authorized()
            if user.has_role_in(*roles) or user.is_superuser:
                return view_func(request, *args, **kwargs)
            return view_forbidden()
        return wrapper
    return decorator
