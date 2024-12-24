from django.db import models
from productos.models import Producto

class Stock(models.Model):
    bodega = models.ForeignKey('Bodega', related_name='stocks', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='stocks', on_delete=models.CASCADE)
    cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_en_transito = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Opcional para movimientos en tránsito
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('bodega', 'producto')  # Garantiza unicidad para bodega y producto

    def __str__(self):
        return f"{self.bodega.nombre} - {self.producto.nombre}: {self.cantidad_disponible}"


class Bodega(models.Model):
    TIPOS = [
        ('INTERNA', 'Interna'),
        ('EXTERNA', 'Externa'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    propietario = models.CharField(max_length=100, blank=True, null=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

