from django.db import models
from django.utils import timezone
from datetime import datetime
from InventariX.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict


# Create your models here.
class Categoria(models.Model):
    id= models.CharField(primary_key=True,max_length=4)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return self.nombre
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Producto(models.Model):
    id= models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    imagen = models.ImageField(upload_to='imagenes/',verbose_name="Imagen")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')
    stock = models.IntegerField(verbose_name='Stock', null=True) 
    precio_compra = models.IntegerField(verbose_name='Precio_compra',null=True)
    precio_venta = models.IntegerField(verbose_name='Precio_venta',null=True)
    agregado = models.DateTimeField(default=timezone.now, verbose_name='Agregado',null=True)
    lugar = models.CharField(max_length=100, verbose_name='Lugar',null=True)



    def __str__(self):
        fila = "Nombre" + self.nombre 
        return self.nombre
    
    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['imagen'] = self.get_image()
        item['precio_venta'] = format(self.precio_venta, '.2f')
        return item
    
    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')   
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
   


class Sale(models.Model):
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.date_joined
    
    def toJSON(self):
        item = model_to_dict(self)
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']
