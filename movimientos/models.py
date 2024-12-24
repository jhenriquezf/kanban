from django.db import models
from bodegas.models import Bodega, Stock
from productos.models import Producto
from ventas.models import LineaNotaVenta
from django.core.exceptions import ValidationError

class MovimientoInventario(models.Model):
    TIPOS_MOVIMIENTO = [
        ('SALIDA', 'Salida'),
        ('ENTRADA', 'Entrada'),
        ('CONSUMO', 'Consumo'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_salida')
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_entrada')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barras_escaneado = models.CharField(max_length=50, null=True, blank=True)
    linea_nota_venta = models.ForeignKey(LineaNotaVenta, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        # Validar que la cantidad sea positiva
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")

        # Validar que la bodega de origen tenga suficiente stock para SALIDA o CONSUMO
        if self.tipo_movimiento in ['SALIDA', 'CONSUMO'] and self.bodega_origen:
            stock = Stock.objects.filter(bodega=self.bodega_origen, producto=self.producto).first()
            if not stock or stock.cantidad_disponible < self.cantidad:
                raise ValidationError("Stock insuficiente en la bodega de origen.")

        # Validar que se especifique una bodega destino para ENTRADA
        if self.tipo_movimiento == 'ENTRADA' and not self.bodega_destino:
            raise ValidationError("Debe especificar una bodega de destino para el movimiento de tipo ENTRADA.")

        # Validar que no haya bodega destino para CONSUMO
        if self.tipo_movimiento == 'CONSUMO' and self.bodega_destino:
            raise ValidationError("No debe especificar una bodega de destino para movimientos de tipo CONSUMO.")

    def save(self, *args, **kwargs):
        # Llamar al método clean antes de guardar
        self.clean()
        super().save(*args, **kwargs)

