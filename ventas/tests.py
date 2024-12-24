from django.test import TestCase
from bodegas.models import Bodega
from productos.models import Producto
from ventas.models import NotaVenta, LineaNotaVenta
from django.core.exceptions import ValidationError

class NotaVentaTestCase(TestCase):

    def setUp(self):
        # Crear bodegas
        self.bodega_origen = Bodega.objects.create(nombre="Bodega Interna", tipo="INTERNA")
        self.bodega_destino = Bodega.objects.create(nombre="Bodega Cliente", tipo="EXTERNA")

        # Crear producto
        self.producto = Producto.objects.create(nombre="Producto B", codigo_barras="987654321")

    def test_nota_venta_consignacion_sin_bodega_destino(self):
        # Intentar crear una nota de venta por consignación sin bodega de destino
        nota_venta = NotaVenta(
            tipo_venta="CONSIGNACION",
            cliente="Cliente X",
            bodega_origen=self.bodega_origen
        )
        with self.assertRaises(ValidationError):
            nota_venta.full_clean()

    def test_linea_nota_venta_valida(self):
        # Crear nota de venta y línea asociada
        nota_venta = NotaVenta.objects.create(
            tipo_venta="SPOT",
            cliente="Cliente Y",
            bodega_origen=self.bodega_origen
        )
        linea = LineaNotaVenta.objects.create(
            nota_venta=nota_venta,
            producto=self.producto,
            cantidad_solicitada=10,
            cantidad_entregada=5,
            cantidad_recibida_o_consumida=5
        )
        # Verificar que las cantidades son consistentes
        self.assertEqual(linea.cantidad_solicitada, 10)
        self.assertEqual(linea.cantidad_entregada, 5)
        self.assertEqual(linea.cantidad_recibida_o_consumida, 5)

    def test_linea_nota_venta_cantidad_entregada_invalida(self):
        # Intentar crear una línea con cantidad entregada mayor a la solicitada
        nota_venta = NotaVenta.objects.create(
            tipo_venta="SPOT",
            cliente="Cliente Z",
            bodega_origen=self.bodega_origen
        )
        linea = LineaNotaVenta(
            nota_venta=nota_venta,
            producto=self.producto,
            cantidad_solicitada=10,
            cantidad_entregada=15
        )
        with self.assertRaises(ValidationError):
            linea.full_clean()