from django.urls import path
from .views import (
    ZonesView,
    ZoneCategoryView,
    IndexView,
    LoadersView
)

app_name = 'warehouse'

urlpatterns = [
    path(
        'categories/',
        ZoneCategoryView.as_view(),
        name='categories'
        ),

    path(
        '',
        IndexView.as_view(),
        name='index',
    ),

    path(
        'zones/',
        ZonesView.as_view(),
        name='zones'
    ),

    path(
        'loaders/',
        LoadersView.as_view(),
        name='loaders'
    ),
]
