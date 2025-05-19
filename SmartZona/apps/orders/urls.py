from django.urls import path
from .views import IndexView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', OrderDetailView.as_view(), name='detail'),
]