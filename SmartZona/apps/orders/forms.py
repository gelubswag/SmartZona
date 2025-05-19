from django.forms import ModelForm
from .models import Order, OrderItem


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'loader',
            'status',
            ]


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product',
            'quantity',
            ]
