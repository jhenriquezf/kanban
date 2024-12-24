from django.db import models
from bodegas.models import Bodega
from productos.models import Producto

from django.core.exceptions import ValidationError

class NotaVenta(models.Model):
    TIPOS_VENTA = [
        ('SPOT', 'Spot'),
        ('CONSIGNACION', 'Consignación'),
    ]

    ESTADOS = [
        ('CREADA', 'Creada'),
        ('EN_PROCESO', 'En proceso'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    tipo_venta = models.CharField(max_length=20, choices=TIPOS_VENTA)
    cliente = models.CharField(max_length=200)
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='notas_salida', limit_choices_to={'tipo': 'INTERNA'})
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='notas_entrada', null=True, blank=True, limit_choices_to={'tipo': 'EXTERNA'})
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='CREADA')

    def __str__(self):
        return f"Nota {self.id} - {self.tipo_venta} ({self.cliente})"
    def clean(self):
            if self.tipo_venta == 'CONSIGNACION' and not self.bodega_destino:
                raise ValidationError("Debe especificar una bodega de destino para ventas por consignación.")

class LineaNotaVenta(models.Model):
    ESTADOS_LINEA = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_TRANSITO', 'En tránsito'),
        ('ENTREGADA', 'Entregada'),
        ('CONSUMIDA', 'Consumida'),
    ]

    nota_venta = models.ForeignKey(NotaVenta, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_solicitada = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_entregada = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_recibida_o_consumida = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS_LINEA, default='PENDIENTE')

    def __str__(self):
        return f"{self.producto.nombre} - {self.nota_venta.id}"
    
    def clean(self):
        if self.cantidad_entregada > self.cantidad_solicitada:
            raise ValidationError("La cantidad entregada no puede ser mayor que la cantidad solicitada.")
        if self.cantidad_recibida_o_consumida > self.cantidad_entregada:
            raise ValidationError("La cantidad recibida o consumida no puede ser mayor que la cantidad entregada.")
