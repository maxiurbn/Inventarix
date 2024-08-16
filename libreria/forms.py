from datetime import datetime
from django.forms import *
from django import forms
from .models import Producto,Categoria,Sale

class ProductoForm(forms.ModelForm):

    

    class Meta: 
        model= Producto
        fields = ['id','nombre', 'imagen', 'categoria', 'stock','precio_compra','precio_venta','agregado','lugar']
        labels ={
            'id': 'id', 
            'nombre': 'Nombre',
            'imagen': 'Imagen', 
            'categoria': 'Categoria', 
            'stock': 'Stock',
            'precio_compra': 'Precio_compra',
            'precio_venta': 'Precio_venta',
            'agregado': 'Agregado',
            'lugar': 'Lugar',
        }
        widgets={
            'id': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese id', 
                    'id': 'id'
                }
            ), 
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese imagen', 
                    'id': 'nombre'
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Seleccione imagen', 
                    'id': 'imagen'
                }
            ), 
            'categoria': forms.Select(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Seleccione categoria', 
                    'id': 'categoria'
                }
            ), 
            'stock': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '000',
                    'id': 'stock',
                }
            ), 
            'precio_compra': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': '000', 
                    'id': 'precio_compra'
                }
            ), 
            'precio_venta': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': '000', 
                    'id': 'precio_venta'
                }
            ), 
            'agregado': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'id': 'agregado'
                }
            ), 
            'lugar': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Describa lugar', 
                    'id': 'lugar'
                }
            )

        }
        

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }