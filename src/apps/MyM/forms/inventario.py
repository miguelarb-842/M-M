from django import forms
from django.forms import formset_factory

from ..models import TipoMovimiento, Variante


class MovimientoInventarioForm(forms.Form):
    """
    Propósito:
        Cabecera de un movimiento de inventario: tipo y descripción.
        Los detalles (variante + cantidad) van en DetalleMovimientoFormSet.

    Returns:
        MovimientoInventarioForm: tipo_movimiento y descripcion.
    """

    tipo_movimiento = forms.ModelChoiceField(
        queryset=TipoMovimiento.objects.all(),
        label='Tipo de movimiento',
        empty_label='Selecciona una opción',
    )
    descripcion = forms.CharField(
        required=False,
        label='Descripción',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Motivo del movimiento'}),
    )


class DetalleMovimientoForm(forms.Form):
    """
    Propósito:
        Una línea de detalle de un movimiento: variante y cantidad.

    Returns:
        DetalleMovimientoForm: variante y cantidad.
    """

    variante = forms.ModelChoiceField(
        queryset=Variante.objects.all(),
        label='Variante',
        empty_label='Selecciona una opción',
    )
    cantidad = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        label='Cantidad',
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
    )


DetalleMovimientoFormSet = formset_factory(DetalleMovimientoForm, extra=1, can_delete=True)
