from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MovimientoInventario
from bodegas.models import Stock

@receiver(post_save, sender=MovimientoInventario)
def actualizar_stock_post_movimiento(sender, instance, created, **kwargs):
    if not created:
        return  # Solo manejar nuevos movimientos

    movimiento = instance
    producto = movimiento.producto

    # Obtenemos o creamos el Stock en la bodega origen
    if movimiento.tipo_movimiento == "SALIDA" and movimiento.bodega_origen:
        stock_origen, created = Stock.objects.get_or_create(
            bodega=movimiento.bodega_origen,
            producto=producto,
            defaults={'cantidad_disponible': 0, 'cantidad_en_transito': 0}
        )
        if stock_origen.cantidad_disponible < movimiento.cantidad:
            raise ValueError("Stock insuficiente para realizar el movimiento.")
        stock_origen.cantidad_disponible -= movimiento.cantidad
        stock_origen.save()

    # Obtenemos o creamos el Stock en la bodega destino
    if movimiento.tipo_movimiento == "ENTRADA" and movimiento.bodega_destino:
        stock_destino, created = Stock.objects.get_or_create(
            bodega=movimiento.bodega_destino,
            producto=producto,
            defaults={'cantidad_disponible': 0, 'cantidad_en_transito': 0}
        )
        stock_destino.cantidad_disponible += movimiento.cantidad
        stock_destino.save()

    # Consumo directo (en ventas por consignación)
    if movimiento.tipo_movimiento == "CONSUMO" and movimiento.bodega_origen:
        stock_origen, created = Stock.objects.get_or_create(
            bodega=movimiento.bodega_origen,
            producto=producto,
            defaults={'cantidad_disponible': 0, 'cantidad_en_transito': 0}
        )
        if stock_origen.cantidad_disponible < movimiento.cantidad:
            raise ValueError("Stock insuficiente para registrar el consumo.")
        stock_origen.cantidad_disponible -= movimiento.cantidad
        stock_origen.save()
