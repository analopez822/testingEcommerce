from core.base_page import BasePage
from core.vocabulario import Boton
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
        self._aviso_carrito_invitado: str = "Tu carrito se guarda en este navegador. Inicia sesión para llevarlo contigo."

    def abrir_producto(self, producto: str) -> None:
        """Busca el producto por texto y abre su ficha (el slug de la URL coincide con el texto buscado)."""
        self.fill_box(self._cajita_busqueda, producto)
        self.encontrar(f"a[href='/catalogo/producto-{producto}']").nth(0).click()

    def aniadir_unidad(self) -> None:
        self.click_boton(self._boton_aniadir_unidad)

    def aniadir_al_carrito(self, nombre_producto: str) -> None:
        """Pulsa 'Añadir al carrito' y comprueba el toast con el nombre del producto."""
        self.click_boton(self._boton_aniadir_carrito)
        self.debe_ver(f'"{nombre_producto}" añadido al carrito')

    def ir_a_finalizar_compra(self) -> None:
        self.click_link(Boton.FINALIZAR_COMPRA)
