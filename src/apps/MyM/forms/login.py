from django import forms


class LoginForm(forms.Form):
    """
    Propósito:
        Formulario de inicio de sesión con nombre de usuario y contraseña.

    Returns:
        LoginForm: Formulario con los campos username y password.
    """

    username = forms.CharField(
        max_length=128,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        label='Contraseña',
    )
