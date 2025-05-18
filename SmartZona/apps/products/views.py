from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator

from SmartZona.utils import model_crud
from SmartZona.apps.users.decorators import allowed_roles
from .models import Product, ProductCategory
from .forms import ProductForm, ProductCategoryForm


@method_decorator(allowed_roles(['manager']), 'dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'products/index.html')


@method_decorator(allowed_roles(['manager']), 'dispatch')
class ProductCategoryView(View):
    def get(self, request):
        return model_crud(
            request,
            ProductCategoryForm,
            ProductCategory,
            'products/product_category.html'
            )

    def post(self, request):
        return model_crud(
            request,
            ProductCategoryForm,
            ProductCategory,
            'products/product_category.html'
            )


@method_decorator(allowed_roles(['manager']), 'dispatch')
class ProductsView(View):
    def get(self, request):
        return model_crud(
            request,
            ProductForm,
            Product,
            'products/products.html'
            )

    def post(self, request):
        return model_crud(
            request,
            ProductForm,
            Product,
            'products/products.html'
            )
