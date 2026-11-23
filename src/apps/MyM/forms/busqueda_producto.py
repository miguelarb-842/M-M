from django import forms


class BusquedaProductoForm(forms.Form):
    """
    Propósito:
        Preparar el campo de búsqueda que utilizará el catálogo para filtrar
        productos por nombre cuando se implemente la interfaz del módulo.

    Args:
        No recibe argumentos propios. Django construye el formulario a partir
        de los campos declarados en la clase.

    Returns:
        BusquedaProductoForm: Formulario con un campo de texto opcional.
    """

    q = forms.CharField(
        required=False,
        label='Buscar producto',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del producto'}),
    )
