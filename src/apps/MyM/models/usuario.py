from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models

from .audit import Auditoria, check_auditoria


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create(self, nombre, password, **extra):
        if not nombre:
            raise ValueError('El usuario debe tener un nombre')
        # shortcut: grupo por defecto 'general' si no se pasan groups (rol obligatorio por convención)
        groups = extra.pop('groups', None) or [Group.objects.get_or_create(name='general')[0]]
        user = self.model(nombre=nombre, **extra)
        user.set_password(password)
        user.save(using=self._db)
        user.groups.set(groups)
        return user

    def create_user(self, nombre, password=None, **extra):
        return self._create(nombre, password, **extra)

    def create_superuser(self, nombre, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self._create(nombre, password, **extra)


class Usuario(AbstractBaseUser, PermissionsMixin, Auditoria):
    # override: el primer usuario se crea sin creador, por eso aquí es opcional
    creado_por = models.ForeignKey('Usuario', on_delete=models.PROTECT, null=True, blank=True, related_name='+')
    # password vive en la columna clave_hash del esquema original
    password = models.CharField(max_length=256, db_column='clave_hash')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, unique=True)
    correo_electronico = models.CharField(max_length=254, unique=True, null=True, blank=True)
    numero_telefonico = models.CharField(max_length=32, null=True, blank=True)
    codigo_telefonico = models.CharField(max_length=8, default='505')
    id_compania_telefonica = models.ForeignKey('CompaniaTelefonica', on_delete=models.PROTECT, null=True, blank=True)

    objects = UsuarioManager()
    USERNAME_FIELD = 'nombre'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'usuario'
        constraints = [check_auditoria('ck_usuario_auditoria')]
