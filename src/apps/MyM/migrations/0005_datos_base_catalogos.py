# Datos base de catálogos.
from django.db import migrations

TIPOS_MOVIMIENTO = [
    ('entrada', ''),
    ('salida', ''),
    ('ajuste positivo', ''),
    ('ajuste negativo', ''),
]

ESTADOS_COMPRA = [
    ('entregada', ''),
    ('pendiente', ''),
    ('cancelada', ''),
]

COMPANIAS_TELEFONICAS = [
    ('tigo', ''),
    ('claro', ''),
]


def crear_datos_base(apps, schema_editor):
    TipoMovimiento = apps.get_model('MyM', 'TipoMovimiento')
    EstadoCompra = apps.get_model('MyM', 'EstadoCompra')
    CompaniaTelefonica = apps.get_model('MyM', 'CompaniaTelefonica')

    for nombre, descripcion in TIPOS_MOVIMIENTO:
        TipoMovimiento.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})

    for nombre, descripcion in ESTADOS_COMPRA:
        EstadoCompra.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})

    for nombre, descripcion in COMPANIAS_TELEFONICAS:
        CompaniaTelefonica.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})


def eliminar_datos_base(apps, schema_editor):
    TipoMovimiento = apps.get_model('MyM', 'TipoMovimiento')
    EstadoCompra = apps.get_model('MyM', 'EstadoCompra')
    CompaniaTelefonica = apps.get_model('MyM', 'CompaniaTelefonica')

    TipoMovimiento.objects.filter(nombre__in=[n for n, _ in TIPOS_MOVIMIENTO]).delete()
    EstadoCompra.objects.filter(nombre__in=[n for n, _ in ESTADOS_COMPRA]).delete()
    CompaniaTelefonica.objects.filter(nombre__in=[n for n, _ in COMPANIAS_TELEFONICAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('MyM', '0004_create_auth_groups'),
    ]

    operations = [
        migrations.RunPython(crear_datos_base, eliminar_datos_base),
    ]
