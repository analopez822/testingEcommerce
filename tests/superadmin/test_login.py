from playwright.sync_api import expect

from conftest import app_login
from pages.shared.login_page import LoginPage

class TestLoginPage:
    """Suite de pruebas para la pagina login"""

    def test_login_exito(self, app_login: LoginPage):
        app_login.navegar("https://cogami.sebcompanyes.com")
        app_login.click_link("Acceder a mi cuenta")
        expect(app_login.buscar_por_texto("Accede a tu cuenta de ")).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_super_admin)
        app_login.fill_box(app_login._password, app_login._contrasenia)
        app_login.click_boton("Entrar")
        expect(app_login.buscar_por_texto("Sesión iniciada correctamente")).to_be_visible()  # toast
        expect(app_login.buscar_por_texto("Resumen general")).to_be_visible()
        app_login.page.wait_for_timeout(2000)

    # def test_login_fallido(self, app_login: LoginPage):
    #     app_login.navegar("https://cogami.sebcompanyes.com/login")
    #     app_login.fill_box(app_login._email, app_login._correo_super_admin)
    #     app_login.fill_box(app_login._password, app_login._contrasenia_incorrecta)
    #     app_login.click_boton("Entrar")
    #     toast = app_login.buscar_por_texto("Email o contraseña incorrectos") # NO SALE en automation
    #     expect(toast).to_be_visible()
    #     app_login.page.wait_for_timeout(2000)
    #
    # def test_mostrar_ocultar_contrasenia(self, app_login: LoginPage):
    #     app_login.navegar("https://cogami.sebcompanyes.com/login")
    #     app_login.fill_box(app_login._password, app_login._contrasenia)
    #     app_login.click_boton_contrasenia("Mostrar contraseña")
    #     app_login.page.wait_for_timeout(2000)
    #     app_login.click_boton_contrasenia("Ocultar contraseña")
    #     app_login.page.wait_for_timeout(2000)
    #
    # def test_reset_password(self, app_login: LoginPage):
    #     app_login.navegar("https://cogami.sebcompanyes.com/login")
    #     app_login.click_link("¿Olvidaste tu contraseña?")
    #     expect(app_login.buscar_por_texto("¿Olvidaste tu contraseña?")).to_be_visible()
    #     app_login.fill_box(app_login._email, app_login._correo_usuario)
    #     app_login.click_boton("Enviar enlace de recuperación")
    #     expect(app_login.buscar_por_texto("Correo enviado")).to_be_visible()
    #     app_login.page.wait_for_timeout(2000)
    #     app_login.click_link("Volver al inicio de sesión")
    #     app_login.page.wait_for_timeout(2000)
    #
    # def test_contacta_con_soporte(self, app_login: LoginPage):
    #     app_login.navegar("https://cogami.sebcompanyes.com/login")
    #     app_login.click_link("Contacta con soporte")
    #     expect(app_login.buscar_por_texto("Envíanos un mensaje")).to_be_visible()
    #     app_login.fill_box(app_login._nombre_completo, "Ana Redondo")
    #     app_login.fill_box(app_login._correo_electronico, app_login._correo_usuario)
    #     app_login.fill_box(app_login._telefono, "123456789")
    #     app_login.fill_box(app_login._asunto, "Problema con la app")
    #     app_login.fill_box(app_login._mensaje, "No puedo iniciar sesión")
    #     app_login.click_boton("Enviar mensaje")
    #     expect(app_login.buscar_por_texto("Hemos recibido tu mensaje. Te responderemos en un plazo máximo de 48 horas.")).to_be_visible()
    #     app_login.page.wait_for_timeout(2000)
    #
    # def test_volver_al_inicio(self, app_login: LoginPage):
    #     app_login.navegar("https://cogami.sebcompanyes.com/login")
    #     app_login.click_link("← Volver al inicio")
    #     expect(app_login.buscar_por_texto("COGAMI En Galicia").nth(0)).to_be_visible()
    #     app_login.page.wait_for_timeout(2000)