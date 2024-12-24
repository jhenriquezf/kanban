from django.test import TestCase
from bodegas.models import Bodega, Stock
from productos.models import Producto
from movimientos.models import MovimientoInventario
from django.core.exceptions import ValidationError

class MovimientoInventarioTestCase(TestCase):

    def setUp(self):
        # Crear bodegas
        self.bodega_interna = Bodega.objects.create(nombre="Bodega Interna", tipo="INTERNA")
        self.bodega_externa = Bodega.objects.create(nombre="Bodega Externa", tipo="EXTERNA")

        # Crear producto
        self.producto = Producto.objects.create(nombre="Producto A", codigo_barras="123456789")

        # Crear stock inicial
        self.stock = Stock.objects.create(bodega=self.bodega_interna, producto=self.producto, cantidad_disponible=100)

    def test_movimiento_salida_valido(self):
        # Crear movimiento de salida válido
        movimiento = MovimientoInventario.objects.create(
            tipo_movimiento="SALIDA",
            bodega_origen=self.bodega_interna,
            producto=self.producto,
            cantidad=50
        )
        # Verificar que el stock disminuye
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.cantidad_disponible, 50)

    def test_movimiento_salida_insuficiente(self):
        # Intentar crear un movimiento con stock insuficiente
        with self.assertRaises(ValidationError):
            MovimientoInventario.objects.create(
                tipo_movimiento="SALIDA",
                bodega_origen=self.bodega_interna,
                producto=self.producto,
                cantidad=200
            )

    def test_movimiento_entrada_valido(self):
        # Crear movimiento de entrada válido
        movimiento = MovimientoInventario.objects.create(
            tipo_movimiento="ENTRADA",
            bodega_destino=self.bodega_externa,
            producto=self.producto,
            cantidad=30
        )
        # Verificar que el stock en la bodega de destino aumenta
        stock_destino = Stock.objects.get(bodega=self.bodega_externa, producto=self.producto)
        self.assertEqual(stock_destino.cantidad_disponible, 30)

    def test_movimiento_consumo_valido(self):
        # Crear movimiento de consumo válido
        movimiento = MovimientoInventario.objects.create(
            tipo_movimiento="CONSUMO",
            bodega_origen=self.bodega_interna,
            producto=self.producto,
            cantidad=20
        )
        # Verificar que el stock disminuye
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.cantidad_disponible, 80)

    def test_movimiento_entrada_sin_bodega_destino(self):
        # Intentar crear un movimiento de entrada sin bodega de destino
        with self.assertRaises(ValidationError):
            MovimientoInventario.objects.create(
                tipo_movimiento="ENTRADA",
                producto=self.producto,
                cantidad=10
            )