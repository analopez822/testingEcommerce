from pages.aplicacion import Aplicacion


class TestNavegacionPage:
    """Suite de pruebas para la pagina de navegacion"""

    def test_inicio(self, app: Aplicacion):
        nav = app.navegacion
        nav.navegar()
        nav.buscar_por_texto(nav._inicio_boton).click()
        nav.debe_ver("Todo lo que necesitas, a un clic")

    def test_catalogo(self, app: Aplicacion):
        app.navegacion.navegar()
        app.navegacion.ir_al_catalogo()
        app.navegacion.debe_ver("Todo lo que tenemos a la venta.")

    def test_novedades(self, app: Aplicacion):
        nav = app.navegacion
        nav.navegar()
        nav.click_link(nav._novedades_boton)
        nav.debe_ver("Lo último de la tienda.")

    def test_contraste(self, app: Aplicacion):
        nav = app.navegacion
        nav.navegar()
        nav.click_boton_contraste(status=nav._contraste_oscuro_boton)
        nav.page.wait_for_timeout(2000)
        nav.click_boton_contraste(status=nav._contraste_claro_boton)
        nav.page.wait_for_timeout(2000)

    def test_carrito(self, app: Aplicacion):
        app.navegacion.navegar()
        app.navegacion.abrir_carrito()
        app.navegacion.debe_ver("Revisa lo que llevas antes de pasar por caja.")

    def test_login(self, app: Aplicacion):
        app.navegacion.navegar()
        app.navegacion.ir_a_login()
        app.navegacion.debe_ver("Iniciar sesión")
