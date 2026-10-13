from playwright.sync_api import expect

from conftest import app_catalogo, app_login, app_navegacion
from pages.shared.catalogo_page import CatalogoPage
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage

class TestCatalogoPage:
    """Suite de pruebas para la pagina catálogo"""

    def test_login_exito(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_catalogo: CatalogoPage):
        app_login.navegar()
        app_navegacion.click_link(app_navegacion._catalogo_boton)
        expect(app_catalogo.buscar_por_texto(app_catalogo._texto_catalogo)).to_be_visible()
        app_catalogo.fill_box(app_catalogo._cajita_busqueda, "chocorramo")
        app_catalogo.encontrar("a[href='/catalogo/producto-chocorramo']").nth(0).click()
        expect(app_catalogo.buscar_por_texto("Disponible")).to_be_visible()
        app_catalogo.click_boton(app_catalogo._boton_aniadir_unidad)
        app_catalogo.click_boton(app_catalogo._boton_aniadir_carrito)
        expect(app_catalogo.buscar_por_texto("\"Chocorramo Unidad\" añadido al carrito")).to_be_visible()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._carrito_boton).click()
        expect(app_catalogo.buscar_por_texto("Tu carrito se guarda en este navegador. Inicia sesión para llevarlo contigo.")).to_be_visible()
        app_catalogo.encontrar("a[href='/checkout']").click()
        # app_catalogo.buscar_por_rol("data-slot", name=app_catalogo._boton_finalizar_compra).click()
        # app_catalogo.click_boton(app_catalogo._boton_finalizar_compra)
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()

        app_catalogo.page.wait_for_timeout(3000)



