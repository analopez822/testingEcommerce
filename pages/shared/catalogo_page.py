from core.base_page import BasePage
from playwright.sync_api import Page

class CatalogoPage(BasePage):
    """
        Clase con los locators y metodos de Catalogo
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators pagina catalogo
        self._texto_catalogo: str = "Todo lo que tenemos a la venta."
        self._cajita_busqueda: str = "input[placeholder='Buscar productos']"
        self._boton_aniadir_unidad: str = "Añadir una unidad"
        self._boton_aniadir_carrito: str = "Añadir al carrito"
        self._boton_finalizar_compra: str = "Finalizar compra"

        # locators pagina finalizar compra
        self._texto_finalizar_compra: str = "Revisa la dirección y confirma el pedido."