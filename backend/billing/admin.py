from django.contrib import admin

from .models import Cliente, Factura, Cobro


# UD3.4b - Administrador del modelo Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'nif', 'email')  # UD3.4a - Columnas que se muestran en la lista
    list_display_links = ('nombre', 'apellidos', 'nif', 'email')  # UD3.4a - Columnas que enlazan a la edición del registro
    list_filter = ('nif',)  # UD3.4a - Filtros del panel lateral derecho
    search_fields = ('nombre', 'apellidos', 'nif', 'email')  # UD3.4a - Campos en los que busca la caja de búsqueda
    preserve_filters = True  # UD3.4a - Mantiene filtros y búsqueda al volver de editar un registro


# UD3.4b - Administrador del modelo Factura
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fecha', 'total')
    list_display_links = ('numero', 'fecha', 'total')
    list_filter = ('cliente',)
    search_fields = ('numero', 'cliente__nombre', 'cliente__apellidos')
    preserve_filters = True


# UD3.4b - Administrador del modelo Cobro
@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = ('factura__numero', 'fecha', 'importe')
    list_display_links = ('factura__numero', 'fecha', 'importe')
    list_filter = ('factura__cliente',)
    search_fields = ('factura__numero', 'factura__cliente__nombre', 'factura__cliente__apellidos')
    preserve_filters = True
