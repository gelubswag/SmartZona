from django.urls import path, include

from .views import UserRegisterView, UserLogoutView, UserLoginView, IndexView


app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name='index')
]
