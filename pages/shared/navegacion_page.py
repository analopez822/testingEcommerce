from core.base_page import BasePage
from playwright.sync_api import Page, Locator, expect

class NavegacionPage(BasePage):
    """
        Clase con los locators y metodos de navegacion que la mayoria de las paginas usan
    """

    def __init__(self, page: Page): # constructor to create new instance of page, a new tab in browser
        super().__init__(page)      # calling constructor of parent class BasePage

        # locators
        self._inicio_boton: str = "Inicio"
        self._catalogo_boton: str = "Catálogo"
        self._novedades_boton: str = "Novedades"
        self._contraste_oscuro_boton: str = "Cambiar a tema claro"
        self._contraste_claro_boton: str = "Cambiar a tema oscuro"
        self._carrito_boton: str = "Abrir carrito" # "/carrito" # '[aria-label="Abrir carrito"]'
        self._login_boton:str = "Iniciar sesión"


    def click_boton_contraste(self, status: str) -> None:
        if status == "Cambiar a tema claro":
            self.page.get_by_role("button", name=self._contraste_oscuro_boton).click()
        elif status == "Cambiar a tema oscuro":
            self.page.get_by_role("button", name=self._contraste_claro_boton).click()


