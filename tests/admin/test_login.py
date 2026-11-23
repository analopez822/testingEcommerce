from core import config
from pages.aplicacion import Aplicacion


class TestLoginPage:
    """Suite de pruebas para la pagina login (rol admin)"""

    def test_login_exito(self, app: Aplicacion):
        nav, login = app.navegacion, app.login
        login.debugger()
        login.navegar()
        nav.ir_a_login()
        login.debe_mostrar_formulario()
        login.alternar_mantener_sesion()
        login.alternar_mantener_sesion()
        login.iniciar_sesion(config.usuario("admin"))
        nav.comprobar_menu_usuario(
            visibles=[nav._mi_cuenta, nav._administracion, nav._cerrar_sesion],
            ocultas=[nav._configuracion],
        )
        login.page.wait_for_timeout(3000)

    def test_login_fallido(self, app: Aplicacion):
        login = app.login
        login.navegar()
        app.navegacion.ir_a_login()
        login.debe_mostrar_formulario()
        login.enviar_credenciales(config.usuario("admin").email, config.CONTRASENIA_INCORRECTA)
        login.debe_ver(login._login_fallido)
