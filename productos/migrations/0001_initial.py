# Generated by Django 5.1.4 on 2024-12-19 22:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='productos.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('codigo_barras', models.CharField(db_index=True, max_length=50, unique=True)),
                ('unidad_medida', models.CharField(default='unidad', max_length=20)),
                ('activo', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='productos.categoria')),
                ('subcategoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='productos.subcategoria')),
            ],
        ),
    ]
