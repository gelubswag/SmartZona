from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator 

from SmartZona.apps.users.decorators import allowed_roles
from .models import Zone, ZoneCategory
from .forms import ZoneForm, ProductCategoryForm


@method_decorator(allowed_roles(['manager']), 'dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'warehouse/index.html')


@method_decorator(allowed_roles(['manager']), 'dispatch')
class ZoneCategoryView(View):
    def get(self, request):
        all_zone_categories = ZoneCategory.objects.all()
        product_category_form = ProductCategoryForm()
        return render(
            request,
            'warehouse/categories.html',
            {
                'categories': all_zone_categories,
                'form': product_category_form
            }
            )

    def post(self, request):
        all_zone_categories = ZoneCategory.objects.all
        zone_category_form = ZoneCategoryForm()
        new_zone_category = ZoneCategoryForm(request.POST)
        error: str | None = None
        if new_zone_category.is_valid() and 'add' in request.POST:
            new_zone_category.save()
        elif not new_zone_category.is_valid and 'add' in request.POST:
            error = "Ошибка при добавлении категории"
        elif 'change' in request.POST:
            category = ZoneCategory.objects.filter(
                id=request.POST['id']
                ).first()
            if category:
                category.name = request.POST['name']
                category.type = request.POST['type']
                category.temperature = request.POST['temperature']
                category.save()
            else:
                error = "Ошибка при изменении категории"
        else:
            category = ZoneCategory.objects.filter(
                id=request.POST['id']
                ).first()
            if category:
                category.delete()
            else:
                error = "Ошибка при удалении категории"
        return render(
            request,
            'warehouse/categories.html',
            {
                'categories': all_zone_categories(),
                'form': zone_category_form,
                'error': error
            }
        )


@method_decorator(allowed_roles(['manager']), 'dispatch')
class ZonesView(View):
    def get(self, request):
        all_zones = Zone.objects.all()
        zone_form = ZoneForm()
        return render(
            request,
            'warehouse/zones.html',
            {
                'zones': all_zones,
                'form': zone_form
            }
            )

    def post(self, request):
        zone_form = ZoneForm()
        new_product = ZoneForm(request.POST)
        error: str | None = None
        if new_product.is_valid() and 'add' in request.POST:
            new_product.save()
        elif not new_product.is_valid() and 'add' in request.POST:
            error = "Ошибка при добавлении товара"
        elif request.POST.get('id') == '':
            error = "Ошибка при изменении товара"
        elif 'change' in request.POST:
            product = Zone.objects.filter(
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
            product = Zone.objects.filter(
                id=request.POST['id']
                ).first()
            if product:
                product.delete()
            else:
                error = "Ошибка при удалении товара"
        return render(
            request,
            'warehouse/zones.html',
            {
                'zones': Zone.objects.all(),
                'form': zone_form,
                'error': error
            }
        )
