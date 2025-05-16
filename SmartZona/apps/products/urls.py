from django.urls import path, include

from .views import ProductCategoryView, IndexView, ProductsView

app_name = 'products'

urlpatterns = [
    path(
        'categories/',
        ProductCategoryView.as_view(),
        name='categories'
        ),

    path(
        '',
        IndexView.as_view(),
        name='index',
    ),

    path(
        'products/',
        ProductsView.as_view(),
        name='products'
    ),
]
