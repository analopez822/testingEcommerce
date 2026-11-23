"""Flujos de sesion: recetas de varios pasos que usan casi todos los tests."""
from core import config
from pages.aplicacion import Aplicacion


def login_como(app: Aplicacion, rol: str) -> None:
    """Abre la tienda, va a 'Iniciar sesión' y entra con el usuario de ese rol ('customer', 'admin', 'superadmin')."""
    app.login.navegar()
    app.navegacion.ir_a_login()
    app.login.debe_mostrar_formulario()
    app.login.iniciar_sesion(config.usuario(rol))


def abrir_mi_cuenta(app: Aplicacion, rol: str = "customer") -> None:
    """Login + Menu de usuario > Mi cuenta."""
    login_como(app, rol)
    app.navegacion.ir_a_mi_cuenta()


def abrir_administracion(app: Aplicacion, rol: str = "superadmin") -> None:
    """Login + Menu de usuario > Administración."""
    login_como(app, rol)
    app.navegacion.ir_a_administracion()
