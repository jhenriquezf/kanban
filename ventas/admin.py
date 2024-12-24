from django.contrib import admin
from .models import NotaVenta, LineaNotaVenta
from .forms import NotaVentaAdminForm

class LineaNotaVentaInline(admin.TabularInline):
    model = LineaNotaVenta
    extra = 1  # Número de líneas vacías que se mostrarán por defecto
    fields = ('producto', 'cantidad_solicitada', 'cantidad_entregada', 'cantidad_recibida_o_consumida', 'estado')
    # Opcionalmente, puedes hacer que algunos campos sean de solo lectura:
    # readonly_fields = ('cantidad_entregada', 'cantidad_recibida_o_consumida')

@admin.register(NotaVenta)
class NotaVentaAdmin(admin.ModelAdmin):
    form = NotaVentaAdminForm
    list_display = ('id', 'tipo_venta', 'cliente', 'bodega_origen', 'bodega_destino', 'fecha_creacion', 'estado')
    list_filter = ('tipo_venta', 'estado')
    search_fields = ('cliente', 'bodega_origen__nombre', 'bodega_destino__nombre')
    date_hierarchy = 'fecha_creacion'
        # Añadimos el Inline a la configuración
    inlines = [LineaNotaVentaInline]
    # Fieldsets para organizar el formulario
    fieldsets = (
        (None, {
            'fields': ('tipo_venta', 'cliente')
        }),
        ('Bodegas', {
            'fields': ('bodega_origen', 'bodega_destino'),
            'description': 'Seleccione la bodega origen y, si es consignación, la bodega destino.'
        }),
        ('Estado', {
            'fields': ('estado',),
        }),
    )
    
    # Añadir acciones personalizadas si se requiere
    actions = ['marcar_como_finalizada']

    def marcar_como_finalizada(self, request, queryset):
        queryset.update(estado='FINALIZADA')
    marcar_como_finalizada.short_description = "Marcar notas seleccionadas como finalizadas"

@admin.register(LineaNotaVenta)
class LineaNotaVentaAdmin(admin.ModelAdmin):
    list_display = ('nota_venta', 'producto', 'cantidad_solicitada', 'cantidad_entregada', 'cantidad_recibida_o_consumida', 'estado')
    list_filter = ('estado',)
    search_fields = ('nota_venta__id', 'producto__nombre')
