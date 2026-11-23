from core import config
from pages.aplicacion import Aplicacion


class TestLoginPage:
    """Suite de pruebas para la pagina login (rol superadmin)"""

    def test_login_exito(self, app: Aplicacion):
        nav, login = app.navegacion, app.login
        login.debugger()
        login.navegar()
        nav.ir_a_login()
        login.debe_mostrar_formulario()
        login.alternar_mantener_sesion()
        login.alternar_mantener_sesion()
        login.iniciar_sesion(config.usuario("superadmin"))
        nav.comprobar_menu_usuario(
            visibles=[nav._mi_cuenta, nav._administracion, nav._configuracion, nav._cerrar_sesion],
        )
        login.page.wait_for_timeout(3000)

    def test_login_fallido(self, app: Aplicacion):
        login = app.login
        login.navegar()
        app.navegacion.ir_a_login()
        login.debe_mostrar_formulario()
        login.enviar_credenciales(config.usuario("superadmin").email, config.CONTRASENIA_INCORRECTA)
        login.debe_ver(login._login_fallido)

    def test_mostrar_ocultar_contrasenia(self, app: Aplicacion):
        login = app.login
        usuario = config.usuario("superadmin")
        login.navegar()
        app.navegacion.ir_a_login()
        login.debe_mostrar_formulario()
        login.fill_box(login._email, usuario.email)
        login.fill_box(login._password, usuario.contrasenia)
        login.click_boton_contrasenia(status=login._boton_contrasenia)
        login.page.wait_for_timeout(2000)
        login.click_boton_contrasenia(status=login._boton_ocultar_contrasenia)
        login.page.wait_for_timeout(2000)
