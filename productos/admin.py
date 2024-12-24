from django.contrib import admin
from .models import Categoria, SubCategoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(SubCategoria)
class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria__nombre')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_barras', 'categoria', 'subcategoria', 'unidad_medida', 'activo')
    list_filter = ('categoria', 'subcategoria', 'activo')
    search_fields = ('nombre', 'codigo_barras')
