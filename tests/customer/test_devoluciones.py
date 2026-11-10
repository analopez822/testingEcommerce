from playwright.sync_api import expect

from conftest import app_login, app_navegacion, app_mi_cuenta
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.mi_cuenta_page import MiCuentaPage
from tests.customer.test_mis_pedidos import TestMisPedidosPage


class TestDevolucionesPage:
    """Suite de pruebas para la pagina Devoluciones"""

    def devoluciones(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
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
        lista_devoluciones = app_mi_cuenta.encontrar("ul[class='flex flex-col gap-3'] > li")   # CSS selector
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

        app_login.page.wait_for_timeout(2000)


    def test_solicitar_devolucion(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        # este test necesita que haya al menos un pedido en la lista de pedidos
        TestMisPedidosPage().mis_pedidos(app_login, app_navegacion, app_mi_cuenta)
        pedido1 = app_mi_cuenta.buscar_por_texto("Pedido P-2026").first.text_content()
        print(pedido1)
        app_mi_cuenta.buscar_por_rol("link", name=app_mi_cuenta._boton_ver_detalle).first.click()
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._link_volver_a_pedidos)).to_be_visible()
        # haciendo click en Devolver
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_devolver_pedido)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._dialogo_devolver_pedido)).to_be_visible()
        app_mi_cuenta.fill_box(app_mi_cuenta._motivo_devolucion, "El producto no cumple con las expectativas")
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_enviar_solicitud)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._confirmacion_solicitud_devolucion)).to_be_visible()
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._no_mas_devoluciones)).to_be_visible()

        # abrir otro browser en incognito para logearse como super admin y aprobar la devolucion
        app_login.debugger()
        browser2 = app_navegacion.abrir_ventana_incognito(close_original_page=False) # para testear chat con los dos browsers abiertos
        admin_navegacion = NavegacionPage(browser2)    # pasando nuevo contexto a clases involucradas en test
        admin_login = LoginPage(browser2)
        admin_mi_cuenta = MiCuentaPage(browser2)
        admin_login.navegar()                          # ???? no entiendo pasar viejo contexto a la nueva ventana incognito
        admin_navegacion.buscar_por_rol("link", name=admin_navegacion._login_boton).click()
        expect(admin_login.buscar_por_texto(admin_login._texto)).to_be_visible()
        admin_login.fill_box(admin_login._email, admin_mi_cuenta._correo_super_admin)
        admin_login.fill_box(admin_login._password, admin_login._contrasenia_super_admin)
        admin_login.buscar_por_rol("button", name=admin_login._boton_entrar).nth(1).click()
        toast = admin_login.buscar_por_texto(admin_login._login_exito)
        expect(toast).to_be_visible()
        admin_navegacion.click_boton(admin_navegacion._menu_usuario_boton)
        admin_navegacion.buscar_por_rol("menuitem", name=admin_navegacion._administracion).click()
        # abriendo Devoluciones y aprobando la solicitud de devolucion
        admin_mi_cuenta.click_link(admin_mi_cuenta._devoluciones)
        expect(admin_mi_cuenta.buscar_por_texto(admin_mi_cuenta._devoluciones_superadmin_header)).to_be_visible()
        # click en acciones de la primera devolucion y despues click en Aprobar
        admin_mi_cuenta.buscar_por_rol("row", name="P-2026-4255 Ana Redondo").get_by_label("Acciones").click()
        admin_mi_cuenta.buscar_por_rol("menuitem", name="Aprobar").click()
        # comprueba que dialogo para aprobar devolucion esta visible y escribe mensaje para el cliente
        expect(admin_mi_cuenta.buscar_por_texto(admin_mi_cuenta._dialogo_aprobar_devolucion)).to_be_visible()
        admin_mi_cuenta.buscar_por_rol("textbox", name="Mensaje para el cliente").fill("Devolucion aprobada")
        # click en boton Aprobar y comprueba que mensaje de devolucion aprobada esta visible
        admin_mi_cuenta.buscar_por_rol("button", name="Aprobar").click()
        expect(admin_mi_cuenta.buscar_por_texto(admin_mi_cuenta._devolucion_aprobada)).to_be_visible()
        # click en acciones de la primera devolucion otra vez y despues click en 'Marcar como recibida'
        admin_mi_cuenta.buscar_por_rol("row", name="P-2026-4255 Ana Redondo").get_by_label("Acciones").click()
        admin_mi_cuenta.buscar_por_rol("menuitem", name="Marcar como recibida").click()
        expect(admin_mi_cuenta.buscar_por_texto(admin_mi_cuenta._stock_repuesto)).to_be_visible()
        # click en acciones de la primera devolucion (por tercera vez) y despues click en Reembolsar
        admin_mi_cuenta.buscar_por_rol("row", name="P-2026-4255 Ana Redondo").get_by_label("Acciones").click()
        admin_mi_cuenta.buscar_por_rol("menuitem", name="Reembolsar").click()
        # comprueba que dialogo para reembolsar devolucion esta visible y click en boton Reembolsar
        expect(admin_mi_cuenta.buscar_por_texto(admin_mi_cuenta._dialogo_reembolso)).to_be_visible()
        admin_mi_cuenta.buscar_por_rol("button", name=admin_mi_cuenta._boton_reembolsar).click()
        # comprueba que dialogo2 para reembolsar devolucion esta visible y click en boton Reembolsar por ultima vez
        expect(admin_mi_cuenta.buscar_por_texto(admin_mi_cuenta._dialogo_reembolso2)).to_be_visible()
        admin_mi_cuenta.buscar_por_rol("button", name=admin_mi_cuenta._boton_reembolsar).click()
        expect(admin_mi_cuenta.buscar_por_texto(admin_mi_cuenta._toast_confirmacion_reembolso)).to_be_visible()
        admin_mi_cuenta.page.wait_for_timeout(5000)


