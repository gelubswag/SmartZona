from django.urls import path, include

from .views import IndexView, DetailSalaryReportView

app_name = 'payroll'

urlpatterns = [
    path(
        '<int:pk>/',
        DetailSalaryReportView.as_view(),
        name='detail'
        ),

    path(
        '',
        IndexView.as_view(),
        name='index',
    ),

    # path(
    #     'products/',
    #     ProductsView.as_view(),
    #     name='products'
    # ),
]
