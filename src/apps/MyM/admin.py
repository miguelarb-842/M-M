from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (Categoria, CompaniaTelefonica, Compra, DetalleCompra,
                     DetalleMovimiento, DetalleVenta, Distribuidor,
                     EstadoCompra, Inventario, Marca, MovimientoInventario,
                     Producto, TipoMovimiento, Usuario, Variante, Venta)


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('nombre', 'password')}),
        ('Perfil', {'fields': ('correo_electronico', 'numero_telefonico',
                               'codigo_telefonico', 'id_compania_telefonica')}),
        ('Estado', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Roles y permisos', {'fields': ('groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {'classes': 'wide', 'fields': ('nombre', 'password1', 'password2')}),
    )
    list_display = ('nombre', 'correo_electronico', 'is_staff', 'is_active')
    search_fields = ('nombre', 'correo_electronico')
    ordering = ('nombre',)
    filter_horizontal = ('groups', 'user_permissions')

    def save_model(self, request, obj, form, change):
        if change:
            # el CHECK de auditoría exige actualizado_por al actualizar
            obj.actualizado_por = request.user
        super().save_model(request, obj, form, change)


class AuditoriaAdmin(admin.ModelAdmin):
    exclude = ('creado_por',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        else:
            obj.actualizado_por = request.user
        super().save_model(request, obj, form, change)


# los roles se gestionan con los grupos de Django (auth_group)

# modelos con bloque de auditoría: la app llena creado_por / actualizado_por
admin.site.register([
    Categoria, Compra, DetalleCompra, DetalleMovimiento, DetalleVenta,
    Distribuidor, Inventario, Marca, MovimientoInventario, Producto,
    Variante, Venta,
], AuditoriaAdmin)

# catálogos simples, sin auditoría
admin.site.register([CompaniaTelefonica, EstadoCompra, TipoMovimiento])
