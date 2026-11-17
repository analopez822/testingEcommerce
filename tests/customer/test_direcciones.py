from playwright.sync_api import expect

from conftest import app_login, app_navegacion, app_mi_cuenta
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.finalizar_compra_page import FinalizarCompraPage
from pages.shared.mi_cuenta_page import MiCuentaPage


class TestDireccionesPage:
    """Suite de pruebas para la pagina Direcciones"""

    def direcciones(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
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
        # abriendo Direcciones y comprobando header
        app_mi_cuenta.click_link(app_mi_cuenta._direcciones)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._direcciones_header)).to_be_visible()
        # contando items en las lista y comprobando que no esta vacia
        lista_direcciones = app_mi_cuenta.encontrar("ul[class='grid gap-4 md:grid-cols-2'] > li")   # CSS selector
        cuenta_direcciones = lista_direcciones.count()

        if cuenta_direcciones > 0:
            print("Existen direcciones")
            print(f"Numero total de direcciones: {cuenta_direcciones}")
            # Iterando sobre todos los elementos y extrayendo direccion
            # .all() resolves the locator to an array of individual element locators
            for item in lista_direcciones.all():
                text = item.text_content()
                print(f"Direccion: {text}")
        else:
            print("No existen direcciones")


    def test_direcciones_eliminar(self, app_login: LoginPage, app_navegacion: NavegacionPage,
                                    app_mi_cuenta: MiCuentaPage):
        # este test necesita que haya al menos dos direcciones en la lista
        self.direcciones(app_login, app_navegacion, app_mi_cuenta)
        # borra la segunda direccion de la lista
        lista_direcciones = app_mi_cuenta.encontrar("ul[class='grid gap-4 md:grid-cols-2'] > li")
        segunda_direccion = lista_direcciones.nth(1) #.text_content()
        #print(f"Segunda direccion: {segunda_direccion}")
        app_mi_cuenta.buscar_por_texto(app_mi_cuenta._boton_eliminar).nth(1).click()
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._dialogo_eliminar)).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_eliminar)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._confirmacion_direccion_eliminada)).to_be_visible()
        expect(segunda_direccion).not_to_be_visible()

    def test_direcciones_editar(self, app_login: LoginPage, app_navegacion: NavegacionPage,
                                    app_mi_cuenta: MiCuentaPage, app_finalizar_compra: FinalizarCompraPage):
        # este test necesita que haya al menos una direccion en la lista
        self.direcciones(app_login, app_navegacion, app_mi_cuenta)
        # edita la primera direccion de la lista
        app_mi_cuenta.buscar_por_texto(app_mi_cuenta._boton_editar).first.click()
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._dialogo_editar)).to_be_visible()
        app_finalizar_compra.fill_box(app_finalizar_compra._provincia, "Barcelona")
        app_finalizar_compra.fill_box(app_finalizar_compra._telefono, "987654321")
        app_finalizar_compra.fill_box(app_finalizar_compra._notas_entrega, "Notas actualizadas")
        app_finalizar_compra.click_boton(app_finalizar_compra._guardar_direccion_boton)
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._direccion_actualizada)).to_be_visible()
        app_mi_cuenta.page.wait_for_timeout(2000)




