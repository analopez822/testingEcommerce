from playwright.sync_api import Page

from components.chat import ChatDialogo
from core.base_page import BasePage
from core.vocabulario import Panel
from pages.shared.cuenta.datos import DatosSeccion
from pages.shared.cuenta.devoluciones import DevolucionesSeccion
from pages.shared.cuenta.direcciones import DireccionesSeccion
from pages.shared.cuenta.pedidos import PedidosSeccion


class MiCuentaPage(BasePage):
    """
    Mi cuenta (y la zona de Administracion, que comparte el panel izquierdo).
    No tiene locators propios: reparte el trabajo entre sus secciones.

        app.mi_cuenta.datos          -> Mis datos
        app.mi_cuenta.pedidos        -> Mis pedidos
        app.mi_cuenta.direcciones    -> Direcciones
        app.mi_cuenta.devoluciones   -> Devoluciones (cliente y superadmin)
        app.mi_cuenta.chat           -> Chat con la tienda
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.datos = DatosSeccion(page)
        self.pedidos = PedidosSeccion(page)
        self.direcciones = DireccionesSeccion(page)
        self.devoluciones = DevolucionesSeccion(page)
        self.chat = ChatDialogo(page)

    def recorrer_panel(self) -> None:
        """Pulsa uno a uno los enlaces del panel izquierdo del cliente."""
        for enlace in Panel.CUENTA_CLIENTE:
            self.click_link(enlace)
