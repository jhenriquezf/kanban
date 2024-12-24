from django import forms
from .models import NotaVenta
from bodegas.models import Bodega

class NotaVentaAdminForm(forms.ModelForm):
    class Meta:
        model = NotaVenta
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        tipo_venta = cleaned_data.get('tipo_venta')
        bodega_destino = cleaned_data.get('bodega_destino')
        
        if tipo_venta == 'CONSIGNACION' and not bodega_destino:
            raise forms.ValidationError("Debe especificar una bodega destino para ventas por consignación.")
        
        return cleaned_data
