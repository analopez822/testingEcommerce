from playwright.sync_api import expect

from conftest import app_login, app_navegacion
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage

class TestLoginPage:
    """Suite de pruebas para la pagina login"""

    def test_login_exito(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_super_admin)
        app_login.fill_box(app_login._password, app_login._contrasenia_super_admin)
        app_login.buscar_por_rol("checkbox", name="Mantener la sesión en este dispositivo").click()
        app_login.buscar_por_rol("checkbox", name="Mantener la sesión en este dispositivo").click()
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        # app_login.buscar_por_texto(app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        # app_login.page.wait_for_timeout(2000)

    def test_login_fallido(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_super_admin)
        app_login.fill_box(app_login._password, app_login._contrasenia_incorrecta)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_fallido)
        expect(toast).to_be_visible()

    def test_mostrar_ocultar_contrasenia(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_super_admin)
        app_login.fill_box(app_login._password, app_login._contrasenia_super_admin)
        app_login.click_boton_contrasenia(status=app_login._boton_contrasenia)
        app_login.page.wait_for_timeout(2000)
        app_login.click_boton_contrasenia(status=app_login._boton_ocultar_contrasenia)
        app_login.page.wait_for_timeout(2000)

    def test_entrar_con_llave_acceso(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.buscar_por_rol("button", name=app_login._entrar_llave_acceso).click()
        app_login.page.wait_for_timeout(3000)
        toast = app_login.buscar_por_texto("Hola de nuevo, Ana")
        expect(toast).to_be_visible()

    def test_reset_password(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.buscar_por_rol("link", name=app_login._link_olvidaste_contrasenia).click()
        expect(app_login.buscar_por_texto(app_login._reset_password)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_enviar_codigo).click()
        expect(app_login.buscar_por_texto(app_login._popup_introducir_codigo)).to_be_visible()
        codigo = input("Introduce el código de verificación recibido por correo electrónico: ")
        app_login.fill_box(app_login._caja_codigo, codigo)   # No sale!!
        app_login.buscar_por_rol("button", name=app_login._boton_continuar).click()
        expect(app_login.buscar_por_texto(app_login._contrasenia_nueva)).to_be_visible()
        app_login.fill_box(app_login._contrasenia, app_login._password_string)
        app_login.fill_box(app_login._repite_contrasenia, app_login._password_string)
        app_login.buscar_por_rol("button", name=app_login._boton_guardar_contrasenia).click()

        expect(app_login.buscar_por_texto(app_login._mensaje_contrasenia_actualizada)).to_be_visible()
        app_login.page.wait_for_timeout(4000)

    def test_reset_password_demasiados_intentos(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()    # terminar
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.buscar_por_rol("link", name=app_login._link_olvidaste_contrasenia).click()
        expect(app_login.buscar_por_texto(app_login._reset_password)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_enviar_codigo).click()
        #expect(app_login.buscar_por_texto(app_login._popup_introducir_codigo)).to_be_visible()
        expect(app_login.buscar_por_texto(app_login._demasiados_intentos)).to_be_visible()

        app_login.page.wait_for_timeout(4000)

    def test_reset_password_volver_a_iniciar_sesion(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.buscar_por_rol("link", name=app_login._link_olvidaste_contrasenia).click()
        expect(app_login.buscar_por_texto(app_login._reset_password)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_super_admin)
        # app_login.buscar_por_rol("button", name=app_login._boton_enviar_codigo).click()
        # expect(app_login.buscar_por_texto(app_login._popup_introducir_codigo)).to_be_visible()
        app_login.buscar_por_rol("link", name=app_login._link_volver_a_iniciar_sesion).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.page.wait_for_timeout(2000)

    def test_crear_cuenta(self, app_login: LoginPage, app_navegacion: NavegacionPage):
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.buscar_por_rol("link", name=app_login._link_crear_cuenta).click()
        expect(app_login.buscar_por_texto(app_login._crear_cuenta)).to_be_visible()

        app_login.fill_box(app_login._nombre, "nombre")
        app_login.fill_box(app_login._apellidos, "apellido")
        mail = input("Introduce el correo electrónico: ")
        app_login.fill_box(app_login._email, mail)
        app_login.fill_box(app_login._contrasenia, app_login._password_string)
        app_login.fill_box(app_login._repite_contrasenia, app_login._password_string)
        app_login.buscar_por_rol("checkbox", name=app_login._tickbox_terminos).click()
        app_login.buscar_por_rol("button", name=app_login._boton_crear_cuenta).click()
        app_login.page.wait_for_timeout(2000)
        expect(app_login.buscar_por_texto(app_login._verifica_correo_nuevo)).to_be_visible()
        codigo = input("Introduce el código de verificación recibido por correo electrónico: ")
        app_login.fill_box(app_login._caja_codigo, codigo)
        app_login.buscar_por_rol("button", name=app_login._boton_verificar).click()
        expect(app_login.buscar_por_texto(app_login._confirmacion_correo_nuevo)).to_be_visible()
        app_login.page.wait_for_timeout(2000)


