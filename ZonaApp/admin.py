from django.contrib import admin
from .models import (
    StaffRole,
    LoaderCategory,
    Loader,
    ZonaStaff,
    Driver,
    ZoneCategory,
    Zone,
    ItemCategory,
    Item,
    Waybill,
    WaybillItem,
    Order,
    OrderItem,
    InventoryReport,
    InventoryReportItem,
    SalaryStatement,
    DecelinedWaybill
)


models = (
    StaffRole,
    LoaderCategory,
    Loader,
    ZonaStaff,
    Driver,
    ZoneCategory,
    Zone,
    ItemCategory,
    Item,
    Waybill,
    WaybillItem,
    Order,
    OrderItem,
    InventoryReport,
    InventoryReportItem,
    SalaryStatement,
    DecelinedWaybill
)

for model in models:
    admin.site.register(model)
