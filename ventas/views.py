from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import ValidationError

from ventas.models import NotaVenta, LineaNotaVenta
from productos.models import Producto
from movimientos.models import MovimientoInventario

@require_POST
@transaction.atomic
def registrar_salida_nota_venta(request):
    nota_venta_id = request.POST.get('nota_venta_id')
    codigo_barras = request.POST.get('codigo_barras')
    cantidad_str = request.POST.get('cantidad')

    if not (nota_venta_id and codigo_barras and cantidad_str):
        return JsonResponse({"error": "Datos incompletos."}, status=400)

    try:
        cantidad = float(cantidad_str)
    except ValueError:
        return JsonResponse({"error": "Cantidad inválida."}, status=400)

    # Obtener la nota de venta
    nota_venta = get_object_or_404(NotaVenta, pk=nota_venta_id)

    # Validar estado de la nota
    if nota_venta.estado not in ["CREADA", "EN_PROCESO"]:
        return JsonResponse({"error": "La Nota de Venta no permite modificaciones en este estado."}, status=400)

    # Obtener el producto por código de barras
    try:
        producto = Producto.objects.get(codigo_barras=codigo_barras, activo=True)
    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado o inactivo."}, status=404)

    # Obtener o crear la línea de la nota de venta para este producto
    linea, creada = LineaNotaVenta.objects.get_or_create(
        nota_venta=nota_venta,
        producto=producto,
        defaults={'cantidad_solicitada': cantidad, 'cantidad_entregada': 0, 'cantidad_recibida_o_consumida': 0}
    )

    # Si la línea ya existía, aumentamos la cantidad solicitada si es necesario
    # En un flujo real, la cantidad_solicitada podría ya estar establecida.
    # Aquí se asume que el escaneo podría aumentar la demanda.
    if not creada and linea.cantidad_solicitada < (linea.cantidad_entregada + cantidad):
        linea.cantidad_solicitada = linea.cantidad_entregada + cantidad

    # Intentar crear el movimiento de inventario (SALIDA)
    try:
        movimiento = MovimientoInventario(
            tipo_movimiento="SALIDA",
            bodega_origen=nota_venta.bodega_origen,
            producto=producto,
            cantidad=cantidad,
            linea_nota_venta=linea
        )
        movimiento.full_clean()  # Validar antes de guardar
        movimiento.save()        # Esto dispara las señales y actualiza el stock
    except ValidationError as e:
        # Error de validación, por ejemplo, stock insuficiente
        return JsonResponse({"error": str(e)}, status=400)

    # Actualizar la línea con la cantidad entregada
    linea.cantidad_entregada += cantidad
    # Ajustar el estado de la línea según las cantidades
    if linea.cantidad_entregada < linea.cantidad_solicitada:
        linea.estado = "PENDIENTE"
    else:
        # Si ya se cumplió la cantidad solicitada, la línea podría considerarse en tránsito o entregada,
        # según la lógica interna. Aquí, por simplicidad, pasamos a EN_TRANSITO.
        linea.estado = "EN_TRANSITO"

    linea.full_clean()
    linea.save()

    # Si todas las líneas están completas, actualizar el estado de la nota_venta
    if all(l.cantidad_entregada >= l.cantidad_solicitada for l in nota_venta.lineas.all()):
        # Podría pasar a EN_PROCESO o incluso marcarla como FINALIZADA si la lógica lo indica
        nota_venta.estado = "EN_PROCESO"
        nota_venta.save()

    return JsonResponse({
        "message": "Salida registrada exitosamente.",
        "nota_venta_id": nota_venta.id,
        "producto": producto.nombre,
        "linea_id": linea.id,
        "cantidad_entregada_linea": float(linea.cantidad_entregada),
        "estado_linea": linea.estado,
        "estado_nota": nota_venta.estado
    }, status=200)
