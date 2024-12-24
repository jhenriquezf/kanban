from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ventas.models import NotaVenta, LineaNotaVenta
from productos.models import Producto
from movimientos.models import MovimientoInventario
from bodegas.models import Bodega


class RegistrarSalidaNotaVentaTest(TestCase):

    def setUp(self):
        # Crear un usuario para autenticación
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Crear bodega
        self.bodega_origen = Bodega.objects.create(nombre="Bodega Central", tipo="INTERNA")

        # Crear un producto
        self.producto = Producto.objects.create(
            nombre="Producto A",
            codigo_barras="123456789",
            activo=True
        )

        # Crear un registro inicial de stock
        MovimientoInventario.objects.create(
            tipo_movimiento="ENTRADA",
            bodega_origen=self.bodega_origen,
            producto=self.producto,
            cantidad=10  # Stock inicial suficiente
        )

        # Crear una Nota de Venta
        self.nota_venta = NotaVenta.objects.create(
            tipo_venta="SPOT",
            cliente="Cliente A",
            bodega_origen=self.bodega_origen
        )

    def test_registrar_salida_exitosamente(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse('registrar_salida_nota_venta'), {
            "nota_venta_id": self.nota_venta.id,
            "codigo_barras": self.producto.codigo_barras,
            "cantidad": "5"
        })
        print(response.json())  # Agregar para depurar la respuesta del servidor
        self.assertEqual(response.status_code, 200)
        self.assertIn("Salida registrada exitosamente.", response.json().get("message"))

        # Verificar que la línea se creó y tiene la cantidad entregada correcta
        linea = LineaNotaVenta.objects.get(nota_venta=self.nota_venta, producto=self.producto)
        self.assertEqual(linea.cantidad_entregada, 5)
        self.assertEqual(linea.estado, "EN_TRANSITO")

    def test_falta_datos(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse('registrar_salida_nota_venta'), {
            "nota_venta_id": self.nota_venta.id,
            "codigo_barras": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Datos incompletos.", response.json().get("error"))

    def test_producto_inactivo(self):
        self.client.login(username="testuser", password="testpass")
        self.producto.activo = False
        self.producto.save()

        response = self.client.post(reverse('registrar_salida_nota_venta'), {
            "nota_venta_id": self.nota_venta.id,
            "codigo_barras": self.producto.codigo_barras,
            "cantidad": "5"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn("Producto no encontrado o inactivo.", response.json().get("error"))

    def test_nota_venta_estado_invalido(self):
        self.client.login(username="testuser", password="testpass")
        self.nota_venta.estado = "FINALIZADA"
        self.nota_venta.save()

        response = self.client.post(reverse('registrar_salida_nota_venta'), {
            "nota_venta_id": self.nota_venta.id,
            "codigo_barras": self.producto.codigo_barras,
            "cantidad": "5"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("La Nota de Venta no permite modificaciones en este estado.", response.json().get("error"))
