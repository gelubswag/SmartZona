from django.urls import path, include

from .views import UserRegisterView, UserLoginView, IndexView


app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('', IndexView.as_view(), name='index')
]
