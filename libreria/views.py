import json
import os
from django.shortcuts import render, redirect
from .models import Producto, Categoria, Sale, DetSale
from django.http import JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from django.template.loader import get_template
from .forms import ProductoForm, CategoriaForm, SaleForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DeleteView, View
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render
from .models import Sale
from xhtml2pdf import pisa

# Create your views here.
def inicio(request):
    return HttpResponse('paginas/index.html')

def index(request):
    productos = Producto.objects.all()
    cantidad_productos = productos.count()
    categorias = Categoria.objects.all()
    cantidad_categorias = categorias.count()
    return render(request,'paginas/index.html',{'cantidad_productos': cantidad_productos,'cantidad_categorias': cantidad_categorias,'productos': productos,'categorias': categorias})

def productos(request):
    productos = Producto.objects.all()
    cantidad_productos = productos.count()
    busqueda = request.GET.get("buscar")
    if busqueda:
        productos = Producto.objects.filter(
            Q(nombre__icontains = busqueda) |
            Q(categoria__nombre__icontains = busqueda) |
            Q(stock__icontains = busqueda) |
            Q(precio_venta__icontains = busqueda) |
            Q(agregado__icontains = busqueda) |
            Q(lugar__icontains = busqueda)
        ).distinct()
    return render(request,'productos/home_productos.html', {'productos': productos, 'cantidad_productos': cantidad_productos})

def crear(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('productos')
    return render(request,'productos/crear.html', {'formulario': formulario})

def editar(request, id):
    producto = Producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('productos')
    return render(request,'productos/editar_producto.html', {'formulario': formulario})

def eliminar(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('productos')
    

def categorias(request):
    categorias = Categoria.objects.all()
    
    busqueda2 = request.GET.get("buscarc")
    if busqueda2:
        categorias = Categoria.objects.filter(
            Q(nombre__icontains = busqueda2) 
        ).distinct()
    return render(request,'categorias/home_categorias.html', {'categorias': categorias})

def crear_categoria(request):
    formulario = CategoriaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('categorias')
    return render(request,'categorias/crear_categoria.html', {'formulario': formulario})

def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    formulario = CategoriaForm(request.POST or None, request.FILES or None, instance=categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('categorias')
    return render(request,'categorias/editar_categoria.html', {'formulario': formulario})

def eliminar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('categorias')



"""aqui ventas nmas"""

class SaleListView(ListView):
    model = Sale
    template_name = 'sale/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('sale_create')
        context['list_url'] = reverse_lazy('sale_list')
        context['entity'] = 'Ventas'
        return context
    
class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('sale_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['precio_venta'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


    
class SaleDeleteView( DeleteView ):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('sale_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context


class SaleInvoicePdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/invoice.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'ALGORISOFT S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('sale_list'))
