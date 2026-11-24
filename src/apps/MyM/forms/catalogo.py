from decimal import Decimal

from django import forms
from django.forms import formset_factory

from ..models import Marca, Categoria


class MarcaForm(forms.Form):
    """
    Propósito:
        Formulario para registrar una marca.

    Returns:
        MarcaForm: nombre y descripción.
    """

    nombre = forms.CharField(
        max_length=128,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de la marca'}),
    )
    descripcion = forms.CharField(
        max_length=254,
        required=False,
        label='Descripción',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción opcional'}),
    )


class CategoriaForm(forms.Form):
    """
    Propósito:
        Formulario para registrar una categoría.

    Returns:
        CategoriaForm: nombre y descripción.
    """

    nombre = forms.CharField(
        max_length=128,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de la categoría'}),
    )
    descripcion = forms.CharField(
        max_length=254,
        required=False,
        label='Descripción',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción opcional'}),
    )


class ProductoForm(forms.Form):
    """
    Propósito:
        Cabecera del formulario para registrar un producto con sus variantes.
        Las variantes van en VarianteFormSet.

    Returns:
        ProductoForm: nombre, descripción, marca y categoría.
    """

    nombre = forms.CharField(
        max_length=254,
        required=True,
        label='Nombre del producto',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del producto'}),
    )
    descripcion = forms.CharField(
        max_length=254,
        required=False,
        label='Descripción',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción opcional'}),
    )
    id_marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        label='Marca',
        empty_label='Selecciona una marca',
    )
    id_categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        label='Categoría',
        empty_label='Selecciona una categoría',
    )


class VarianteForm(forms.Form):
    """
    Propósito:
        Una línea de detalle de un producto: nombre, descripción y stock
        mínimo de la variante. El stock mínimo se guarda en la tabla de
        inventario de la variante.

    Returns:
        VarianteForm: nombre, descripcion y stock_minimo.
    """

    nombre = forms.CharField(
        max_length=128,
        required=True,
        label='Nombre de la variante',
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Talla M'}),
    )
    descripcion = forms.CharField(
        max_length=254,
        required=False,
        label='Descripción',
        widget=forms.TextInput(attrs={'placeholder': 'Descripción opcional'}),
    )
    stock_minimo = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        required=False,
        initial=Decimal('0'),
        label='Stock mínimo',
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': '0'}),
    )
    id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )


VarianteFormSet = formset_factory(VarianteForm, extra=1, can_delete=True)
