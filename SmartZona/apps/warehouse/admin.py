from django.contrib import admin

from .models import Zone, ZoneCategory, Loader

admin.site.register(ZoneCategory)
admin.site.register(Zone)
admin.site.register(Loader)
