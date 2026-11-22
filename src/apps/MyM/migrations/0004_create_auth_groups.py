# Groups for role-based access control with model permissions.
from django.db import migrations

# Cada grupo: lista de (nombre_modelo, [acciones]).
# Acciones: add, change, delete, view.
GROUPS_PERMISOS = {
    'gestor_de_ventas': [
        ('venta', ['add', 'change', 'delete', 'view']),
        ('detalleventa', ['add', 'change', 'delete', 'view']),
    ],
    'gestor_de_compras': [
        ('compra', ['add', 'change', 'delete', 'view']),
        ('detallecompra', ['add', 'change', 'delete', 'view']),
        ('distribuidor', ['add', 'change', 'delete', 'view']),
        ('estadocompra', ['add', 'change', 'delete', 'view']),
    ],
    'gestor_de_productos': [
        ('producto', ['add', 'change', 'delete', 'view']),
        ('variante', ['add', 'change', 'delete', 'view']),
        ('marca', ['add', 'change', 'delete', 'view']),
        ('categoria', ['add', 'change', 'delete', 'view']),
    ],
    'gestor_de_inventario': [
        ('inventario', ['add', 'change', 'delete', 'view']),
        ('movimientoinventario', ['add', 'change', 'delete', 'view']),
        ('tipomovimiento', ['add', 'change', 'delete', 'view']),
        ('compra', ['view']),
        ('venta', ['view']),
    ],
}


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    for group_name, model_perms in GROUPS_PERMISOS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        perms = []
        for model_name, actions in model_perms:
            ct = ContentType.objects.get(app_label='MyM', model=model_name)
            for action in actions:
                codename = f'{action}_{model_name}'
                perm = Permission.objects.get(content_type=ct, codename=codename)
                perms.append(perm)
        group.permissions.set(perms)


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=list(GROUPS_PERMISOS.keys())).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('MyM', '0003_alter_usuario_correo_electronico'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]
