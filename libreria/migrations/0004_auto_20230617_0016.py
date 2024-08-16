# Generated by Django 3.0.4 on 2023-06-17 04:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0003_remove_producto_descriprion_producto_agregado_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='categoria',
            options={'ordering': ['id'], 'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['id'], 'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterField(
            model_name='categoria',
            name='id',
            field=models.CharField(max_length=4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.Categoria', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(upload_to='imagenes/', verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.CreateModel(
            name='DetSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cant', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.Producto')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.Sale')),
            ],
            options={
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalle de Ventas',
                'ordering': ['id'],
            },
        ),
    ]
