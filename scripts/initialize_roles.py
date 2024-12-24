from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ventas.models import NotaVenta
from movimientos.models import MovimientoInventario

def create_roles_and_permissions():
    # Vendedor
    vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')
    vendedor_permissions = [
        Permission.objects.get(codename='add_notaventa'),  # Permiso para crear Nota de Venta
        Permission.objects.get(codename='change_notaventa'),
        Permission.objects.get(codename='view_notaventa'),
    ]
    vendedor_group.permissions.set(vendedor_permissions)

    # Bodeguero Interno
    bodeguero_interno_group, _ = Group.objects.get_or_create(name='Bodeguero Interno')
    bodeguero_interno_permissions = [
        Permission.objects.get(codename='view_notaventa'),  # Puede ver las Notas de Venta
        Permission.objects.get(codename='add_movimientoinventario'),  # Registrar salidas
        Permission.objects.get(codename='view_movimientoinventario'),
    ]
    bodeguero_interno_group.permissions.set(bodeguero_interno_permissions)

    # Bodeguero Externo
    bodeguero_externo_group, _ = Group.objects.get_or_create(name='Bodeguero Externo')
    bodeguero_externo_permissions = [
        Permission.objects.get(codename='view_notaventa'),  # Puede ver las Notas de Venta
        Permission.objects.get(codename='add_movimientoinventario'),  # Registrar entradas
    ]
    bodeguero_externo_group.permissions.set(bodeguero_externo_permissions)

    # Usuario Final
    usuario_final_group, _ = Group.objects.get_or_create(name='Usuario Final')
    usuario_final_permissions = [
        Permission.objects.get(codename='view_notaventa'),
        Permission.objects.get(codename='add_movimientoinventario'),  # Registrar consumos
    ]
    usuario_final_group.permissions.set(usuario_final_permissions)

    print("Roles y permisos creados correctamente.")
