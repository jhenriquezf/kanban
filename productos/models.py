from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo_barras = models.CharField(max_length=50, unique=True, db_index=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True, blank=True)
    unidad_medida = models.CharField(max_length=20, default="unidad")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
