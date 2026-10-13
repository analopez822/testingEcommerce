from playwright.sync_api import expect

from conftest import app_navegacion
from pages.shared.navegacion_page import NavegacionPage

class TestNavegacionPage:
    """Suite de pruebas para la pagina de navegacion"""

    def test_inicio(self, app_navegacion: NavegacionPage):
        app_navegacion.navegar()
        app_navegacion.buscar_por_texto(app_navegacion._inicio_boton).click()
        expect(app_navegacion.buscar_por_texto("Todo lo que necesitas, a un clic")).to_be_visible()

    def test_catalogo(self, app_navegacion: NavegacionPage):
        app_navegacion.navegar()
        app_navegacion.click_link(app_navegacion._catalogo_boton)
        expect(app_navegacion.buscar_por_texto("Todo lo que tenemos a la venta.")).to_be_visible()

    def test_novedades(self, app_navegacion: NavegacionPage):
        app_navegacion.navegar()
        app_navegacion.click_link(app_navegacion._novedades_boton)
        expect(app_navegacion.buscar_por_texto("Lo último de la tienda.")).to_be_visible()

    def test_contraste(self, app_navegacion: NavegacionPage):
        app_navegacion.navegar()
        app_navegacion.click_boton_contraste(status= app_navegacion._contraste_oscuro_boton)
        app_navegacion.page.wait_for_timeout(2000)
        app_navegacion.click_boton_contraste(status= app_navegacion._contraste_claro_boton)
        app_navegacion.page.wait_for_timeout(2000)

    def test_carrito(self, app_navegacion: NavegacionPage):
        app_navegacion.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._carrito_boton).click()
        # app_navegacion.click_link(app_navegacion._carrito_boton) ==> cambiar a "self._carrito_boton: str = "/carrito"" en navegacion_page.py
        # y uncomment esta linea en click_link() method de base_page.py: self.page.locator(f'a[href*="{texto}"]').click()
        expect(app_navegacion.buscar_por_texto("Revisa lo que llevas antes de pasar por caja.")).to_be_visible()

    def test_login(self, app_navegacion: NavegacionPage):
        app_navegacion.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_navegacion.buscar_por_texto("Iniciar sesión")).to_be_visible()









