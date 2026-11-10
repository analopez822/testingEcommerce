from playwright.sync_api import expect

from conftest import app_login, app_navegacion, app_mi_cuenta
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.mi_cuenta_page import MiCuentaPage


class TestChatPage:
    """Suite de pruebas para el Chat"""

    def test_chat_devolucion(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        # No hace falta que exista un pedido con pago pendiente
        # se requiere que haya una sesion abierta para el usuario
        # y una segunda sesion para el super admin
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()

        # preguntar en chat
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_chat)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._dialogo_chat_con_tienda)).to_be_visible()
        app_mi_cuenta.buscar_por_placeholder(app_mi_cuenta._caja_mensaje_chat).fill("Como se realiza una devolucion?")
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_enviar_chat)
        expect(app_mi_cuenta.buscar_por_texto("Como se realiza una devolucion?").first).to_be_visible()
        app_mi_cuenta.page.wait_for_timeout(2000)

        # abrir otro browser en incognito para contestar en chat
        browser2 = app_navegacion.abrir_ventana_incognito(close_original_page=False) # para testear chat con los dos browsers abiertos
        admin_navegacion = NavegacionPage(browser2)    # pasando nuevo contexto a clases involucradas en test
        admin_login = LoginPage(browser2)
        admin_mi_cuenta = MiCuentaPage(browser2)
        admin_login.navegar()
        admin_navegacion.buscar_por_rol("link", name=admin_navegacion._login_boton).click()
        expect(admin_login.buscar_por_texto(admin_login._texto)).to_be_visible()
        admin_login.fill_box(admin_login._email, admin_mi_cuenta._correo_super_admin)
        admin_login.fill_box(admin_login._password, admin_login._contrasenia_super_admin)
        admin_login.buscar_por_rol("button", name=admin_login._boton_entrar).nth(1).click()
        toast = admin_login.buscar_por_texto(admin_login._login_exito)
        expect(toast).to_be_visible()
        admin_navegacion.click_boton(admin_navegacion._menu_usuario_boton)
        # abriendo Administracion y luego Chat de usuario especifico
        admin_navegacion.buscar_por_rol("menuitem", name=admin_navegacion._administracion).click()
        admin_mi_cuenta.click_link(admin_mi_cuenta._chat)
        boton_usuario = admin_mi_cuenta.encontrar(admin_mi_cuenta._boton_chat_usuario)
        boton_usuario = boton_usuario.filter(has_text="Ana").first
        expect(boton_usuario).to_be_visible()
        boton_usuario.click()
        # escribiendo mensaje en chat para usuario y enviando
        app_mi_cuenta.buscar_por_placeholder(app_mi_cuenta._caja_mensaje_chat).fill("Abre el pedido y haz click en Devolver")
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_enviar_chat)
        admin_mi_cuenta.page.wait_for_timeout(3000)

        # volviendo al primer browser para comprobar que el mensaje del super admin se ve en el chat del usuario
        app_mi_cuenta.page.bring_to_front()
        # leyendo el ultimo mensaje en el chat del usuario y comprobando que es el mismo que envio el super admin
        lista_mensajes = app_mi_cuenta.encontrar(app_mi_cuenta._mensajes_en_chat).page.locator("ul[class='flex flex-col gap-3'] > li").last
        text = lista_mensajes.text_content()
        print(f"Ultimo mensaje en chat: {text}")
        expect(lista_mensajes).to_contain_text("Abre el pedido y haz click en Devolver")




