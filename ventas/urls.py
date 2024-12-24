from django.urls import path
from .views import registrar_salida_nota_venta

urlpatterns = [
    path('registrar_salida/', registrar_salida_nota_venta, name='registrar_salida'),
]
