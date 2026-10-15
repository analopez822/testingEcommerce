from playwright.sync_api import expect

from conftest import app_login, app_navegacion
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage

class TestLoginPage:
    """Suite de pruebas para la pagina login"""

    def test_login_exito(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.debugger()
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_admin)
        app_login.fill_box(app_login._password, app_login._contrasenia_admin)
        app_login.buscar_por_rol("checkbox", name="Mantener la sesión en este dispositivo").click()
        app_login.buscar_por_rol("checkbox", name="Mantener la sesión en este dispositivo").click()
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        app_login.click_boton("Menú de usuario")
        expect(app_login.buscar_por_rol("menuitem", name="Mi cuenta")).to_be_visible()
        expect(app_login.buscar_por_rol("menuitem", name="Administración")).to_be_visible()
        expect(app_login.buscar_por_rol("menuitem", name="Configuración")).not_to_be_visible()
        expect(app_login.buscar_por_rol("menuitem", name="Cerrar sesión")).to_be_visible()
        app_login.page.wait_for_timeout(3000)

    def test_login_fallido(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_admin)
        app_login.fill_box(app_login._password, app_login._contrasenia_incorrecta)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_fallido)
        expect(toast).to_be_visible()

    # def test_reset_password(self, app_login: LoginPage, app_navegacion: NavegacionPage):
    #     """ Requiere meter manualmente el codigo enviado al correo """
    #     app_login.navegar()
    #     app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
    #     expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
    #     app_login.buscar_por_rol("link", name=app_login._link_olvidaste_contrasenia).click()
    #     expect(app_login.buscar_por_texto(app_login._reset_password)).to_be_visible()
    #     app_login.fill_box(app_login._email, app_login._correo_admin)   #_correo_usuario
    #     app_login.buscar_por_rol("button", name=app_login._boton_enviar_codigo).click()
    #     expect(app_login.buscar_por_texto(app_login._popup_introducir_codigo)).to_be_visible()
    #     codigo = input("Introduce el código de verificación recibido por correo electrónico: ")
    #     app_login.fill_box(app_login._caja_codigo, codigo)   # No sale!!
    #     app_login.buscar_por_rol("button", name=app_login._boton_continuar).click()
    #     app_login.page.wait_for_timeout(3000)
    #     expect(app_login.buscar_por_texto(app_login._contrasenia_nueva)).to_be_visible()
    #     app_login.fill_box(app_login._contrasenia, app_login._password_string)
    #     app_login.fill_box(app_login._repite_contrasenia, app_login._password_string)
    #     app_login.buscar_por_rol("button", name=app_login._boton_guardar_contrasenia).click()
    #     expect(app_login.buscar_por_texto(app_login._mensaje_contrasenia_actualizada)).to_be_visible()
    #     app_login.fill_box(app_login._email, app_login._correo_admin)
    #     app_login.fill_box(app_login._password, app_login._password_string)
    #     app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
    #     toast = app_login.buscar_por_texto(app_login._login_exito)
    #     expect(toast).to_be_visible()
    #     app_login.page.wait_for_timeout(4000)






