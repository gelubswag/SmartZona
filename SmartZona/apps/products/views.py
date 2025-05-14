from django.shortcuts import render
from django.views import View

from apps.users.decorators import allowed_roles
from .models import Product, ProductCategory
from .forms import ProductForm, ProductCategoryForm


class ProductsView(View):
    @allowed_roles(['manager'])
    def get(self, request):
        all_products = Product.objects.all()
        product_form = ProductForm()
        # TODO: create template
        # return render(request, 'products/products.html', {'products': all_products})

    def post(self, request):
        new_product = ProductForm(request.POST)
        error: str | None = None
        if new_product.is_valid():
            new_product.instance.user = request.user
            new_product.save()
            error = "Ошибка при добавлении продукта"

        return self.get(request)
    
