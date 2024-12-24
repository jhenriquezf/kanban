from django.contrib import admin
from .models import Bodega, Stock

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'propietario', 'ubicacion', 'activo')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre', 'propietario', 'ubicacion')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('bodega', 'producto', 'cantidad_disponible', 'cantidad_en_transito', 'ultima_actualizacion')
    list_filter = ('bodega',)
    search_fields = ('bodega__nombre', 'producto__nombre')
