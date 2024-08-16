from django.urls import path, include
from . import views
from .views import SaleCreateView, SaleListView, SaleDeleteView, SaleInvoicePdfView
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('productos',views.productos,name='productos'),
    path('productos/crear',views.crear,name='crear'),
    path('productos/editar',views.editar,name='editar'),
    path('eliminar/<int:id>',views.eliminar,name='eliminar'),
    path('productos/editar/<int:id>',views.editar,name='editar'),  
    path('categorias',views.categorias,name='categorias'),
    path('categorias/crear_categoria',views.crear_categoria,name='crear_categoria'),
    path('categorias/editar_categoria',views.editar_categoria,name='editar_categoria'),
    path('eliminar_categoria/<int:id>',views.eliminar_categoria,name='eliminar_categoria'),
    path('categorias/editar_categoria/<int:id>',views.editar_categoria,name='editar_categoria'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()