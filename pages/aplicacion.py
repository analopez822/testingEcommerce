from functools import cached_property

from playwright.sync_api import Page

from pages.shared.catalogo_page import CatalogoPage
from pages.shared.finalizar_compra_page import FinalizarCompraPage
from pages.shared.login_page import LoginPage
from pages.shared.mi_cuenta_page import MiCuentaPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.pago_tarjeta_page import PagoTarjetaPage
from pages.shared.recibo_pedido_page import ReciboPedidoPage


class Aplicacion:
    """
    La tienda vista desde UNA ventana del navegador. Reparte las pages a los tests:

        def test_algo(self, app: Aplicacion):
            app.login.navegar()
            app.navegacion.ir_a_login()

    Una pagina nueva = 3 lineas aqui (ni fixture nueva ni imports en cada test).
    Se crea cada page solo cuando se usa por primera vez.
    """

    def __init__(self, page: Page):
        self.page = page

    @cached_property
    def login(self) -> LoginPage:
        return LoginPage(self.page)

    @cached_property
    def navegacion(self) -> NavegacionPage:
        return NavegacionPage(self.page)

    @cached_property
    def catalogo(self) -> CatalogoPage:
        return CatalogoPage(self.page)

    @cached_property
    def finalizar_compra(self) -> FinalizarCompraPage:
        return FinalizarCompraPage(self.page)

    @cached_property
    def pago_tarjeta(self) -> PagoTarjetaPage:
        return PagoTarjetaPage(self.page)

    @cached_property
    def recibo_pedido(self) -> ReciboPedidoPage:
        return ReciboPedidoPage(self.page)

    @cached_property
    def mi_cuenta(self) -> MiCuentaPage:
        return MiCuentaPage(self.page)

    def nueva_sesion(self) -> "Aplicacion":
        """Abre otra ventana en incognito (sin cookies) con su propia Aplicacion. Util para probar dos usuarios a la vez."""
        return Aplicacion(self.login.abrir_ventana_incognito(close_original_page=False))
