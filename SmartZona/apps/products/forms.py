from django.forms import ModelForm
from .models import Product, ProductCategory


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'article',
            'category',
            'unit',
            'expiration_date',
            'storage_temperature',
            'zone',
            'quantity'
            ]

class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = [
            'name',
            'zone_category'
            ]