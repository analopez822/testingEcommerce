"""Flujos de 'Mi cuenta': dejan al test en la pantalla lista para probar."""
from flows.auth import abrir_mi_cuenta
from pages.aplicacion import Aplicacion


def abrir_pedidos(app: Aplicacion) -> None:
    """Login (cliente) > Mi cuenta > Mis pedidos, mostrando por consola lo que hay en la lista."""
    abrir_mi_cuenta(app)
    app.mi_cuenta.pedidos.abrir()
    app.mi_cuenta.pedidos.describir()


def abrir_primer_pedido(app: Aplicacion) -> str:
    """Igual que abrir_pedidos pero entrando en el detalle del primer pedido. Devuelve su texto."""
    abrir_pedidos(app)
    return app.mi_cuenta.pedidos.abrir_primer_pedido()


def abrir_direcciones(app: Aplicacion) -> None:
    """Login (cliente) > Mi cuenta > Direcciones, mostrando por consola lo que hay en la lista."""
    abrir_mi_cuenta(app)
    app.mi_cuenta.direcciones.abrir()
    app.mi_cuenta.direcciones.describir()
