from django import forms
from .models import MovimientoInventario
from productos.models import Producto

class MovimientoInventarioAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MovimientoInventarioAdminForm, self).__init__(*args, **kwargs)
        # Filtrar solo productos activos
        self.fields['producto'].queryset = Producto.objects.filter(activo=True)

    class Meta:
        model = MovimientoInventario
        fields = '__all__'
