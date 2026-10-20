from core.base_page import BasePage
from playwright.sync_api import Page

class ReciboPedidoPage(BasePage):
    """
        Clase con los locators y metodos de Recibo Pedido
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators pagina recibo pedido
        self._texto_recibo: str = "Recibo del pedido"
        self._texto_producto_pagado: str = "Producto"
