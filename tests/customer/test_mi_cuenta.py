from playwright.sync_api import expect

from conftest import app_login, app_navegacion, app_mi_cuenta
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.mi_cuenta_page import MiCuentaPage


class TestMiCuentaPage:
    """Suite de pruebas para la pagina login"""

    def test_mi_cuenta(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        #app_login.debugger()
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        # comprobando titulo y secciones de Mis Datos
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._texto_mis_datos)).to_be_visible()
        # expect(app_mi_cuenta.buscar_por_placeholder(app_mi_cuenta._datos_personales)).to_be_visible()
        # expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._correo)).to_be_visible()
        # expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._descargar_datos)).to_be_visible()
        # expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._eliminar_cuenta)).to_be_visible()

        # comprobando elementos de panel izquierdo: abriendo y verificando titulo
        app_mi_cuenta.click_link(app_mi_cuenta._mis_datos)
        app_mi_cuenta.click_link(app_mi_cuenta._mis_pedidos)
        app_mi_cuenta.click_link(app_mi_cuenta._direcciones)
        app_mi_cuenta.click_link(app_mi_cuenta._metodos_pago)
        app_mi_cuenta.click_link(app_mi_cuenta._devoluciones)
        app_mi_cuenta.click_link(app_mi_cuenta._seguridad)
        app_mi_cuenta.click_link(app_mi_cuenta._soporte)
        app_login.page.wait_for_timeout(2000)



