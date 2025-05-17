from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator 

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
        all_product_categories = ProductCategory.objects.all()
        product_category_form = ProductCategoryForm()
        return render(
            request,
            'products/product_category.html',
            {
                'categories': all_product_categories,
                'form': product_category_form
            }
            )

    def post(self, request):
        all_product_categories = ProductCategory.objects.all
        product_category_form = ProductCategoryForm()
        new_product_category = ProductCategoryForm(request.POST)
        error: str | None = None
        if new_product_category.is_valid() and 'add' in request.POST:
            new_product_category.save()
        elif not new_product_category.is_valid and 'add' in request.POST:
            error = "Ошибка при добавлении категории"
        elif 'change' in request.POST:
            category = ProductCategory.objects.filter(
                id=request.POST['id']
                ).first()
            if category:
                category.name = request.POST['name']
                category.zone_category = request.POST['zone_category']
                category.save()
            else:
                error = "Ошибка при изменении категории"
        else:
            category = ProductCategory.objects.filter(
                id=request.POST['id']
                ).first()
            if category:
                category.delete()
            else:
                error = "Ошибка при удалении категории"
        return render(
            request,
            'products/product_category.html',
            {
                'categories': all_product_categories(),
                'form': product_category_form,
                'error': error
            }
        )


@method_decorator(allowed_roles(['manager']), 'dispatch')
class ProductsView(View):
    def get(self, request):
        all_products = Product.objects.all()
        product_form = ProductForm()
        return render(
            request,
            'products/products.html',
            {
                'products': all_products,
                'form': product_form
            }
            )

    def post(self, request):
        product_form = ProductForm()
        new_product = ProductForm(request.POST)
        error: str | None = None
        if new_product.is_valid() and 'add' in request.POST:
            new_product.save()
        elif not new_product.is_valid() and 'add' in request.POST:
            error = "Ошибка при добавлении товара"
        elif request.POST.get('id') == '':
            error = "Ошибка при изменении товара"
        elif 'change' in request.POST:
            product = Product.objects.filter(
                id=request.POST['id']
                ).first()
            if product:
                product.name = request.POST['name']
                product.article = request.POST['article']
                product.category = request.POST['category']
                product.unit = request.POST['unit']
                product.expiration_date = request.POST['expiration_date']
                product.zone = request.POST['zone']
                product.quantity = request.POST['quantity']
                product.storage_temperature = request.POST[
                    'storage_temperature'
                    ]
                product.save()
            else:
                error = "Ошибка при изменении товара"
        else:
            product = Product.objects.filter(
                id=request.POST['id']
                ).first()
            if product:
                product.delete()
            else:
                error = "Ошибка при удалении товара"
        return render(
            request,
            'products/products.html',
            {
                'products': Product.objects.all(),
                'form': product_form,
                'error': error
            }
        )
