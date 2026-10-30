from playwright.sync_api import expect

from conftest import app_login, app_navegacion, app_mi_cuenta
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.mi_cuenta_page import MiCuentaPage


class TestDevolucionesPage:
    """Suite de pruebas para la pagina Devoluciones"""

    def test_devoluciones(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        # app_login.debugger()
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        app_navegacion.click_boton(app_navegacion._menu_usuario_boton)
        app_navegacion.buscar_por_rol("menuitem", name=app_navegacion._mi_cuenta).click()
        # abriendo Devoluciones y comprobando header
        app_mi_cuenta.click_link(app_mi_cuenta._devoluciones)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._devoluciones_header)).to_be_visible()
        # contando items en las lista y comprobando que no esta vacia
        lista_devoluciones = app_mi_cuenta.encontrar("ul[class='grid gap-4 md:grid-cols-2'] > li")   # CSS selector
        cuenta_devoluciones = lista_devoluciones.count()

        if cuenta_devoluciones > 0:
            print("Existen devoluciones")
            print(f"Numero total de devoluciones: {cuenta_devoluciones}")
            # Iterando sobre todos los elementos y extrayendo direccion
            # .all() resolves the locator to an array of individual element locators
            for item in lista_devoluciones.all():
                text = item.text_content()
                print(f"Devolucion: {text}")
        else:
            print("No existen devoluciones")



