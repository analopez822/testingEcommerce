from playwright.sync_api import expect
from pydantic import json

from conftest import app_login, app_navegacion, app_mi_cuenta
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.mi_cuenta_page import MiCuentaPage


class TestMisPedidosPage:
    """Suite de pruebas para la pagina Mis Pedidos"""

    def mis_pedidos(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
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
        # abriendo Mis Pedidos y comprobando header
        app_mi_cuenta.click_link(app_mi_cuenta._mis_pedidos)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._pedidos_header)).to_be_visible()
        # contando items en las lista y comprobando que no esta vacia
        lista_pedidos = app_mi_cuenta.encontrar("ul[class='flex flex-col gap-3'] > li")   # CSS selector
        cuenta_pedidos = lista_pedidos.count()

        if cuenta_pedidos > 0:
            print("Existen pedidos")
            print(f"Numero total de pedidos: {cuenta_pedidos}")
            # Iterando sobre todos los elementos y extrayendo nombre pedido
            # .all() resolves the locator to an array of individual element locators
            for item in lista_pedidos.all():
                text = item.text_content()
                print(f"Informacion del pedido: {text}")
        else:
            print("No existen pedidos")


    def test_mis_pedidos_pago_prueba(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        # necesita que exista un pago pendiente, y que sea el primero de la lista
        self.mis_pedidos(app_login, app_navegacion, app_mi_cuenta)
        pedido1 = app_mi_cuenta.buscar_por_texto("Pedido P-2026").first.text_content()
        print(pedido1)
        app_mi_cuenta.buscar_por_rol("link", name=app_mi_cuenta._boton_ver_detalle).first.click()
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._link_volver_a_pedidos)).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_pago_prueba)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._dialogo_pago_prueba)).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_pago_correcto)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._pago_completado)).to_be_visible()
        app_mi_cuenta.page.wait_for_timeout(3000)


    def test_mis_pedidos_descargar_recibo_chat(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        # No hace falta que exista un pedido con pago pendiente, este test funciona en cualquier pedido
        self.mis_pedidos(app_login, app_navegacion, app_mi_cuenta)
        pedido1 = app_mi_cuenta.buscar_por_texto("Pedido P-2026").first.text_content()
        print(pedido1)
        # bajar recibo
        app_mi_cuenta.buscar_por_rol("link", name=app_mi_cuenta._boton_ver_detalle).first.click()
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._link_volver_a_pedidos)).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_descargar_recibo)

        ruta_recibo = app_mi_cuenta.descargar_pdf(app_mi_cuenta._boton_descargar_recibo)
        assert ruta_recibo.exists(), f"El recibo no existe en la ruta: {ruta_recibo}"
        print(f"Recibo descargado en: {ruta_recibo}")
        app_mi_cuenta.abrir_archivo(ruta_recibo)

        # preguntar en chat
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_chat)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._dialogo_chat_con_tienda)).to_be_visible()
        app_mi_cuenta.buscar_por_placeholder(app_mi_cuenta._caja_mensaje_chat).fill("Como se realiza una devolucion?")
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_enviar_chat)
        expect(app_mi_cuenta.buscar_por_texto("Como se realiza una devolucion?").first).to_be_visible()
        app_mi_cuenta.page.wait_for_timeout(3000)


    def test_mis_pedidos_cancelar(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        # necesita que el primer pedido de la lista no este cancelado. Se podria mejorar buscando el nombre del pedido
        self.mis_pedidos(app_login, app_navegacion, app_mi_cuenta)
        pedido1 = app_mi_cuenta.buscar_por_texto("Pedido P-2026").first.text_content()
        print(pedido1)
        app_mi_cuenta.buscar_por_rol("link", name=app_mi_cuenta._boton_ver_detalle).first.click()
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._link_volver_a_pedidos)).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_cancelar_pedido)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._dialogo_cancelar_pedido)).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_cancelar_pedido)
        expect(app_mi_cuenta.buscar_por_texto(f"{pedido1} {app_mi_cuenta._confirmacion_pedido_cancelado}"))
        app_mi_cuenta.page.wait_for_timeout(3000)





