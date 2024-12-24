from django import forms
from .models import MovimientoInventario
from bodegas.models import Stock
from .forms import MovimientoInventarioAdminForm

class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        tipo_movimiento = cleaned_data.get('tipo_movimiento')
        bodega_origen = cleaned_data.get('bodega_origen')
        bodega_destino = cleaned_data.get('bodega_destino')
        cantidad = cleaned_data.get('cantidad')
        producto = cleaned_data.get('producto')

        # Validaciones adicionales si es necesario
        if tipo_movimiento == 'SALIDA' and bodega_origen:
            stock = Stock.objects.filter(bodega=bodega_origen, producto=producto).first()
            if not stock or stock.cantidad_disponible < cantidad:
                raise forms.ValidationError("Stock insuficiente en la bodega de origen.")

        return cleaned_data

# Registrar en el admin
from django.contrib import admin
from .models import MovimientoInventario

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    form = MovimientoInventarioAdminForm
    list_display = ('id', 'tipo_movimiento', 'producto', 'bodega_origen', 'bodega_destino', 'cantidad', 'fecha')
    list_filter = ('tipo_movimiento', 'fecha')
    search_fields = ('producto__nombre', 'bodega_origen__nombre', 'bodega_destino__nombre')
    date_hierarchy = 'fecha'

