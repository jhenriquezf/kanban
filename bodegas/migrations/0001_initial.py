# Generated by Django 5.1.4 on 2024-12-19 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('INTERNA', 'Interna'), ('EXTERNA', 'Externa')], max_length=50)),
                ('propietario', models.CharField(blank=True, max_length=100, null=True)),
                ('ubicacion', models.CharField(blank=True, max_length=255, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
    ]
