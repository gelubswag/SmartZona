from django.forms import ModelForm
from .models import Zone, ZoneCategory, Loader


class ZoneForm(ModelForm):
    class Meta:
        model = Zone
        fields = [
            'code',
            'category',
            'capacity',
            ]


class ZoneCategoryForm(ModelForm):
    class Meta:
        model = ZoneCategory
        fields = [
            'name',
            'type',
            'temperature'
            ]


class LoaderForm(ModelForm):
    class Meta:
        model = Loader
        fields = [
            'type',
            'load_capacity',
            'is_available'
            ]
