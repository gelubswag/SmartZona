from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from .forms import UserRegisterForm, UserLoginForm
from .utils import get_user_from_post, set_active


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(
            request,
            'users/auth.html',
            {'form': form, 'title': 'Регистрация'}
            )

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('users:login')
        error = form.errors
        return render(
            request,
            'users/auth.html',
            {
                'form': form,
                'error': error,
                'title': 'Регистрация',
            }
            )


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(
            request,
            'users/auth.html',
            {'form': form, 'title': 'Вход'}
            )

    def post(self, request):
        form = UserLoginForm(request.POST)
        user = authenticate(
            request,
            **get_user_from_post(request),
            )
        if user:
            login(request, user)
            return redirect('users:index')
        error = "Пользователь не найден или пароль неверный"
        return render(
            request,
            'users/auth.html',
            {
                'form': form,
                'error': error,
                'title': 'Вход',
            }
            )


class IndexView(View):
    def get(self, request):
        ctx = {}

        set_active(ctx, 'index')
        return render(
            request,
            'users/index.html',
            ctx
            )


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')
