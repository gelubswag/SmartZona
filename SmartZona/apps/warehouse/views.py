from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator 

from SmartZona.utils import model_crud
from SmartZona.apps.users.decorators import allowed_roles
from .models import Zone, ZoneCategory, Loader
from .forms import ZoneForm, ZoneCategoryForm, LoaderForm


@method_decorator(allowed_roles(['manager']), 'dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'warehouse/index.html')


@method_decorator(allowed_roles(['manager']), 'dispatch')
class ZoneCategoryView(View):
    def get(self, request):
        return model_crud(
            request,
            ZoneCategoryForm,
            ZoneCategory,
            'warehouse/categories.html',
            )

    def post(self, request):
        return model_crud(
            request,
            ZoneCategoryForm,
            ZoneCategory,
            'warehouse/categories.html',
            )


@method_decorator(allowed_roles(['manager']), 'dispatch')
class ZonesView(View):
    def get(self, request):
        return model_crud(
            request,
            ZoneForm,
            Zone,
            'warehouse/zones.html',
            )

    def post(self, request):
        return model_crud(
            request,
            ZoneForm,
            Zone,
            'warehouse/zones.html',
            )


@method_decorator(allowed_roles(['manager']), 'dispatch')
class LoadersView(View):
    def get(self, request):
        return model_crud(
            request,
            LoaderForm,
            Loader,
            'warehouse/loaders.html',
            )

    def post(self, request):
        return model_crud(
            request,
            LoaderForm,
            Loader,
            'warehouse/loaders.html',
            )
